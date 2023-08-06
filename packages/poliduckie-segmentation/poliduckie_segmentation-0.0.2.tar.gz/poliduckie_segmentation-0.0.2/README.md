# poliduckie_segmentation
A package ready to be installed that provides the segmentation work made by the Poliduckie team

### Example
```python
from poliduckie_segmentation.segmentation import Segmentation

image = [...]
segmentation = Segmentation()

# To predict:
prediction = segmentation.predict(image)

# To get the model:
segmentation.get_model()

# To get the model summary:
segmentation.get_model_summary()
```
