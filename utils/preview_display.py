import time
from IPython import display
from PIL import Image


class PreviewDisplay:
  """Periodically display the given image in Colab.

  A class is needed because it seems we cannot simply assign to a variable
  inside with gil: in prange(), and instead need to call a method of an object.
  """

  def __init__(self, every_n_sec: float, image_width: int, image_height: int):
    self.last_display_time_in_sec = time.perf_counter()
    self.every_n_sec = every_n_sec
    # I cannot find a way to build PIL Image directly on top of a bytearray.
    # Instead, the best I can do is to cast a bytearray to bytes, and set that
    # to a PIL Image. This probably involves copying the output image twice per
    # update, which is not ideal.
    self.preview_image = Image.new('RGB', (image_width, image_height))
    self.display_id = 'preview'
    display.display(self.preview_image, display_id=self.display_id)

  def _should_render(self):
    """Returns True if it has been at least |every_n_sec| since the last time
    this method returns True."""
    new_time_in_seconds = time.perf_counter()
    if new_time_in_seconds - self.last_display_time_in_sec < self.every_n_sec:
      return False
    self.last_display_time_in_sec = new_time_in_seconds
    return True

  def update(self, buffer: bytearray):
    self.preview_image.frombytes(bytes(buffer), 'raw', 'RGB', 0, 1)
    display.update_display(self.preview_image, display_id=self.display_id)

  def maybe_update(self, buffer: bytearray):
    if self._should_render():
      self.update(buffer)

  def get_image(self):
    return self.preview_image
