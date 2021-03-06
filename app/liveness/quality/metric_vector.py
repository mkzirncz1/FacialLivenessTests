from abc import ABC, abstractmethod
from liveness.quality.metrics.generic import AbstractQualityMetric, AbstractNoReferenceQualityMetric
from joblib import Parallel, delayed


class AbstractMetricVectorCreator(ABC):
    def __init__(self, metrics):
        self.metrics = metrics

    @abstractmethod
    def create_vector(self, input_img, blurred_image):
        pass


def get_metric_output(m, input_img, blurred_image):
    value = None

    if isinstance(m, AbstractNoReferenceQualityMetric):
        # if no reference, just pass input_img.

        value = m.calculate(input_img)
        print(value)
    elif isinstance(m, AbstractQualityMetric):
        # if abstract quality metric, pass both images

        value = m.calculate(input_img, blurred_image)

    return value


class DefaultMetricVectorCreator(AbstractMetricVectorCreator):
    def create_vector(self, input_img, blurred_image):
        metric_vector = Parallel(n_jobs=4, require='sharedmem', prefer='threads')(
            delayed(get_metric_output)(m, input_img, blurred_image) for m in self.metrics
        )

        return metric_vector
