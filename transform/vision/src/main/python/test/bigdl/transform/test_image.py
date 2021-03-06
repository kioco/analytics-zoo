# from bigdl.transform.vision.image import *

import pytest
import os
from bigdl.util.common import *
from transform.vision.image import *


class TestLayer():

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        sparkConf = create_spark_conf()
        self.sc = SparkContext(master="local[4]", appName="test model",
                               conf=sparkConf)
        init_engine()
        resource_path = os.path.join(os.path.split(__file__)[0], "../resources")
        self.image_path = os.path.join(resource_path, "image/000025.jpg")

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        self.sc.stop()

    def transformer_test(self, transformer):
        image_frame = ImageFrame.read(self.image_path)
        transformer(image_frame)
        image_frame.transform(transformer)
        image_frame.to_sample()

        image_frame = ImageFrame.read(self.image_path, self.sc)
        transformer(image_frame)
        image_frame.transform(transformer)
        sample = image_frame.to_sample()
        sample.count()

    def test_colorjitter(self):
        color = ColorJitter(random_order_prob=1.0, shuffle=True)
        self.transformer_test(color)

    def test_resize(self):
        resize = Resize(200, 200, 1)
        self.transformer_test(resize)

    def test_fixed_crop_norm(self):
        crop = FixedCrop(0.0, 0.0, 0.5, 1.0)
        self.transformer_test(crop)

    def test_fixed_crop_unnorm(self):
        crop = FixedCrop(0.0, 0.0, 200.0, 200., False)
        self.transformer_test(crop)

    def test_center_crop(self):
        crop = CenterCrop(200, 200)
        self.transformer_test(crop)

    def test_random_crop(self):
        crop = RandomCrop(200, 200)
        self.transformer_test(crop)

    def test_expand(self):
        expand = Expand(means_r=123, means_g=117, means_b=104,
                        max_expand_ratio=2.0)
        self.transformer_test(expand)

    def test_hflip(self):
        transformer = HFlip()
        self.transformer_test(transformer)

    def test_random_transformer(self):
        transformer = RandomTransformer(HFlip(), 0.5)
        self.transformer_test(transformer)

    def test_pipeline(self):
        transformer = Pipeline([ColorJitter(), HFlip(), Resize(200, 200, 1)])
        self.transformer_test(transformer)

    def test_get_image(self):
        image_frame = ImageFrame.read(self.image_path)
        image_frame.get_image()

    def test_get_label(self):
        image_frame = ImageFrame.read(self.image_path)
        image_frame.get_label()

    def test_to_sample(self):
        image_frame = ImageFrame.read(self.image_path)
        image_frame.to_sample()

    def test_is_local(self):
        image_frame = ImageFrame.read(self.image_path)
        assert image_frame.is_local() is True
        image_frame = ImageFrame.read(self.image_path, self.sc)
        assert image_frame.is_local() is False

    def test_is_distributed(self):
        image_frame = ImageFrame.read(self.image_path)
        assert image_frame.is_distributed() is False
        image_frame = ImageFrame.read(self.image_path, self.sc)
        assert image_frame.is_distributed() is True

if __name__ == "__main__":
    pytest.main([__file__])
