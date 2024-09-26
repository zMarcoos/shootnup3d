from typing import Dict
import time

class Cooldown:
  _cooldowns: Dict[str, float] = {}

  @staticmethod
  def start_cooldown(name: str, duration: float) -> None:
    Cooldown._cooldowns[name] = time.time() + duration

  @staticmethod
  def is_on_cooldown(name: str) -> bool:
    current_time = time.time()
    if name in Cooldown._cooldowns:
      if current_time >= Cooldown._cooldowns[name]:
        del Cooldown._cooldowns[name]
        return False
      return True
    return False

  @staticmethod
  def clear_expired_cooldowns() -> None:
    current_time = time.time()
    expired_cooldowns = [name for name, end_time in Cooldown._cooldowns.items() if current_time >= end_time]
    for name in expired_cooldowns:
      del Cooldown._cooldowns[name]
