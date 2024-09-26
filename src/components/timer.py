from typing import Callable, Tuple, Dict, Optional
import time
import uuid

class Timer:
  _timers: Dict[str, Tuple[float, Callable[[], None]]] = {}

  @staticmethod
  def add_timer(duration: float, callback: Callable[[], None], id: Optional[str] = None) -> str:
    if id is None:
      id = str(uuid.uuid4())
  
    Timer._timers[id] = (time.time() + duration, callback)
    return id

  @staticmethod
  def update_timers() -> None:
    current_time = time.time()
    expired_timers = [id for id, (end_time, _) in Timer._timers.items() if current_time >= end_time]

    for id in expired_timers:
      _, callback = Timer._timers[id]
      callback()
      del Timer._timers[id]

  @staticmethod
  def remove_timer(id: str) -> None:
    if id in Timer._timers:
      del Timer._timers[id]

  @staticmethod
  def get_timer(id: str) -> Tuple[float, Callable[[], None]]:
    return Timer._timers.get(id, (0, None))

  @staticmethod
  def has_timer(id: str) -> bool:
    return id in Timer._timers
