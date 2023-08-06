#!/usr/bin/env python3

import cv2
import time
import numpy as np
import pyrealsense2 as rs
from threading import Timer, Lock

try:
    from class_as_process import class_as_process
    from rs_utils import splice_imgs, merge_depth_image_for_vis
except ModuleNotFoundError:
    from .class_as_process import class_as_process
    from .rs_utils import splice_imgs, merge_depth_image_for_vis


class RealsenseCamera:
    def __init__(self, snid=None, get_frame_method="wait_for_frames", try_num=-1, fps=6):
        if snid is None:
            snid = self.get_all_snids()[0]
        self.lock = Lock()
        self.snid = snid
        self.get_frame_method = get_frame_method
        self.try_num = try_num
        self.fps = fps
        time.sleep(0.1 * np.random.random())
        self.try_run(self.set_config_and_option)

        self.spatial_filter = None
        self.temporal_filter = None

    def robust_get_data(self):
        """may_has_delay"""
        return self.try_run(self.get_data)

    def get_data(self):
        frameset = self.get_frameset()
        data = self.post_processing(frameset)
        return data

    def get_frameset(self):
        with self.lock:
            get_frameset = getattr(self.pipeline, self.get_frame_method)
            frameset = get_frameset()
            return frameset

    def set_config_and_option(self):
        with self.lock:
            # set config
            config = rs.config()
            config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, self.fps)
            config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, self.fps)
            # config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 6)
            # config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 6)
            config.enable_device(self.snid)

            # set pipline
            self.pipeline = rs.pipeline()
            self.profile = self.pipeline.start(config)
            self.device = self.profile.get_device()
            self.color_sensor = self.device.query_sensors()[1]

            # set depth option
            depth_sensor = self.depth_sensor = self.device.first_depth_sensor()

            # set "High Accuracy" depth mode
            depth_sensor.set_option(rs.option.visual_preset, 3)

            # set_laser_power
            power_rate = 1
            depth_sensor.set_option(
                rs.option.laser_power,
                int(
                    depth_sensor.get_option_range(rs.option.laser_power).max
                    * power_rate
                ),
            )

            # set postprocess
            # self.spatial_filter = self.default_spatial_filter
            # self.temporal_filter = self.default_temporal_filter

    align = rs.align(rs.stream.color)
    default_spatial_filter = rs.spatial_filter()
    default_temporal_filter = rs.temporal_filter()

    def post_processing(self, frameset):
        streams = self.profile.get_streams()
        assert frameset.size() == len(streams)
        data = {}
        # Reproject depth from ir cam to RGB cam
        frameset = self.align.process(frameset)
        for stream in streams:
            key = str(stream.stream_type()).replace("stream.", "")
            if rs.stream.infrared == stream.stream_type():
                frame = frameset.get_infrared_frame(stream.stream_index())
                key = key + str(stream.stream_index())
            else:
                frame = frameset.first_or_default(stream.stream_type())
                if stream.stream_type() == rs.stream.depth:
                    if self.spatial_filter:
                        frame = self.spatial_filter.process(frame)
                    if self.temporal_filter:
                        frame = self.temporal_filter.process(frame)
                # data[key+"_info"] = frame.get_profile()
            data[key] = self.frame_to_numpy(frame)
        return data

    @staticmethod
    def frame_to_numpy(frame):
        return np.asanyarray(frame.get_data())

    def try_run(
        self, funcation,
    ):
        n = 0
        while True:
            try:
                n += 1
                return funcation()
            except RuntimeError as e:
                if n == self.try_num:
                    print(
                        f"[snid:{self.snid}] try {funcation} {self.try_num} times, fails!"
                    )
                    raise e
                print(f"[snid:{self.snid}] try {n} time, RuntimeError:")
                print(e)
                # self.hardware_reset()
                try:
                    if "device" not in self.__dict__:
                        devices = list(rs.context().devices)
                        filter_devices = [d for d in devices if self.snid in str(d)]
                        assert (
                            len(filter_devices) == 1
                        ), f"S/N: {self.snid} not in {devices}"
                        self.device = filter_devices[0]
                    self.device.hardware_reset()
                    time.sleep(1.5)
                    """
                    1.5s is a magic number
                    if sleep(1), will need 5s at `pipe.start(config)` after `device.hardware_reset()`
                    """
                except RuntimeError as e:
                    print(f"[snid:{self.snid}] try {n} time, RuntimeError:")
                    print(e)
                    if "No such file or directory" in str(e):
                        pass
                try:
                    self.set_config_and_option()
                except RuntimeError as e:
                    print(f"[snid:{self.snid}] try {n} time, RuntimeError:")
                    print(e)

    def hardware_reset(self):
        """
        To del
        """
        self.device.hardware_reset()
        time.sleep(1.5)
        self.set_config_and_option()

    def set_exposure(self, t, camera="color"):
        if camera == "color":
            device = self.color_sensor
        if camera == "depth":
            device = self.depth_sensor
        t_ms = int(round(t * 1000))
        device.set_option(rs.option.exposure, t_ms)

    @classmethod
    def from_camera_idx(cls, idx=0):
        snids = MultiRealsenseManger.get_all_snids()
        snid = snids[idx]
        return cls(snid)

    @staticmethod
    def get_all_snids(context=None):
        if context is None:
            context = rs.context()
        snids = []
        for d in context.devices:
            if "realsense" in d.get_info(rs.camera_info.name).lower():
                snids.append(d.get_info(rs.camera_info.serial_number))
        return sorted(snids)

    def _get_stream(self, camera="color"):
        for stream in self.profile.get_streams():
            if camera == "color" and stream.format() == rs.format.rgb8:
                break
            if camera == "depth" and stream.format() == rs.format.z16:
                break
        return stream

    def get_intrinsic(self, camera="color"):
        stream = self._get_stream(camera)
        rsi = stream.as_video_stream_profile().get_intrinsics()
        intrinsic = dict(
            fx=rsi.fx,
            fy=rsi.fy,
            cx=rsi.ppx,
            cy=rsi.ppy,
            D=[rsi.coeffs],
            xy=(rsi.width, rsi.height),
        )
        return intrinsic

    def load_settings_json(self, json_path):
        with open(json_path, "r") as file:
            json_text = file.read().strip()
        advanced_mode = rs.rs400_advanced_mode(self.device)
        advanced_mode.load_json(json_text)

    def save_settings_json(self, json_path="/tmp/realsense-settings.json"):
        advanced_mode = rs.rs400_advanced_mode(self.device)
        json_text = advanced_mode.serialize_json()
        with open(json_path, "w") as file:
            file.write(json_text)

    def stop(self):
        self.pipeline.stop()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()


class RealsenseForVis(RealsenseCamera):
    def post_processing(self, frameset):
        data = super().post_processing(frameset)
        # data["vis"] = data["color"]
        data["vis"] = merge_depth_image_for_vis(data)
        return data


class MultiRealsenseManger(dict):
    def __init__(
        self,
        MetaRealsenseClass=RealsenseCamera,
        init_args=None,
        init_kwargs=None,
        dummy=False,
        snids=None,
        init_gap_time=1,
    ):
        """
        Multi-realsense manger with multi-processing
        based on dict

        Parameters
        ----------
        MetaRealsenseClass : TYPE, optional
            Realsense class. The default is RealsenseCamera.
        init_args : tuple, optional
            Init args for MetaRealsenseClass. The default is [].
        init_kwargs : dict, optional
            Init kwargs for MetaRealsenseClass. The default is {}.
        dummy : bool, optional
            If True, using multiprocess.dummy which is multi-threading. 
            The default is False.
        snids : list of str, optional
            List of snids. The default is self.get_all_snids().
        init_gap_time: int, default 1
            init_gap_time
        """

        super().__init__()
        if snids is None:
            snids = MultiRealsenseManger.get_all_snids()
        for snid in snids:
            time.sleep(init_gap_time)
            _kwargs = {} if init_kwargs is None else init_kwargs.copy()
            _kwargs.update(snid=snid)
            self[snid] = class_as_process(
                cls=MetaRealsenseClass,
                init_args=init_args,
                init_kwargs=_kwargs,
                dummy=dummy,
            )

    get_all_snids = RealsenseCamera.get_all_snids

    def __enter__(self):
        return self

    def __exit__(self, *args):
        [process.terminate() for process in self.values()]
        [process.join() for process in self.values()]

    def __getattr__(self, key):
        if not callable(getattr(next(iter(self.values())), key)):
            return {k: getattr(v, key) for k, v in self.items()}

        def func(*args, **kwargs):
            threads = []
            res = {}

            def func(snid, process):
                res[snid] = getattr(process, key)(*args, **kwargs)

            for snid, process in self.items():
                thread = Timer(0, func, (snid, process))
                thread.start()
                threads.append(thread)
            [thread.join() for thread in threads]
            res = {key: res[key] for key in sorted(res)}
            return res

        return func


if __name__ == "__main__":
    """
    Robust multi-processing multi-realsense manager
    
    Usage:
        1. Build a new class based on RealsenseCamera.
        2. Override set_config_and_option and post_processing method
            for custom config and processing.
    
    Example:
        >>> class CustomRealsense(RealsenseCamera):
                def set_config_and_option(self):
                    # edit the config and option 
                    # refer to RealsenseCamera.set_config_and_option
                
                def post_processing(self, frameset):
                    # edit the post processing for frameset
                    # refer to RealsenseCamera.post_processing
                    return data        
    """

    # Example code
    snids = MultiRealsenseManger.get_all_snids()
    print("All realsense snids:", snids)
    MetaRealsenseClass = RealsenseForVis
    FRAME_NUM = 50
    with MetaRealsenseClass(snids[0]) as rc:
        print(f"imshow first realsense's image, {FRAME_NUM} frames")
        for i in range(FRAME_NUM):
            print(f"{i}/{FRAME_NUM}")
            cv2.waitKey(1)
            data = rc.robust_get_data()
            vis = merge_depth_image_for_vis(data)
            cv2.imshow("first camera", vis[..., ::-1])

    with MultiRealsenseManger(MetaRealsenseClass) as mrm:
        for snid in mrm:
            for i in range(FRAME_NUM):
                print(f"snid: {snid}, {i}/{FRAME_NUM}")
                cv2.waitKey(1)
                data = mrm[snid].robust_get_data()
                vis = merge_depth_image_for_vis(data)
                cv2.imshow(f"snid: {snid}", vis[..., ::-1])

        print("\n\n\n imshow multi realsense images")
        while 1:
            _begin = time.time()
            key = cv2.waitKey(1)
            datas = mrm.robust_get_data()
            frame = splice_imgs([data["vis"] for data in datas.values()])
            cv2.imshow(f"{len(mrm)} realsense", frame[..., ::-1])
            if key == ord("q"):
                cv2.destroyAllWindows()
                break
            print("Loop Spend", round(time.time() - _begin, 2))
