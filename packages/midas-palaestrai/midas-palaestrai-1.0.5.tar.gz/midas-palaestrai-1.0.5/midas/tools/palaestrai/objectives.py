from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, List
import logging
from palaestrai.agent import Objective

from .gauss import normal_distribution_pdf

if TYPE_CHECKING:
    from palaestrai.agent import RewardInformation


class PowerGridAttackerObjective(Objective):
    VM_PU_NORM = partial(
        normal_distribution_pdf, mu=1.0, sigma=-0.05, c=-1.2, a=-2.5
    )

    def __init__(self, is_defender=False):
        self.sign_factor = -1.0 if is_defender else 1.0

    def internal_reward(self, rewards: List[RewardInformation]) -> float:
        try:
            max_vm = next(r for r in rewards if r.reward_id == "vm_pu-max")
            median_ll = next(
                r for r in rewards if r.reward_id == "lineload-median"
            )
        except StopIteration:
            return 0.0

        return self.sign_factor * float(
            PowerGridAttackerObjective.VM_PU_NORM(max_vm())
            + 2 * median_ll() / 100.0
        )


class ErikasExcitinglyEvilObjective(Objective):
    """This is really an attacker objective."""

    def __init__(self, report_after=10):
        self.log = logging.getLogger("midas.ErikasExcitinglyEvilObjective")
        self._ctr = 0
        self._report_after = report_after
        self._last_rewards = []
        self.log.info("ErikasExcitinglyEvilObjective loaded")

    def internal_reward(
        self, rewards: List["RewardInformation"], **kwargs
    ) -> float:

        erikas_reward = sum(
            r() for r in rewards if "ErikaReward" in r.reward_id
        )
        self._last_rewards.append(-erikas_reward)
        self._ctr += 1
        if self._ctr >= self._report_after:
            self._ctr -= self._report_after
            self.log.info(f"Last rewards: {self._last_rewards}")
            self._last_rewards = []

        return -erikas_reward


class AndreasAnnoyinglyAmicableObjective(Objective):
    """This is really an defender objective."""

    def __init__(self, report_after=10):
        self.log = logging.getLogger(
            "midas.AndreasAnnoyinglyAmicableObjective"
        )
        self._ctr = 0
        self._report_after = report_after
        self._last_rewards = []
        self.log.info("AndreasAnnoyinglyAmicableObjective loaded")

    def internal_reward(
        self, rewards: List["RewardInformation"], **kwargs
    ) -> float:
        erikas_reward = sum(
            r() for r in rewards if "ErikaReward" in r.reward_id
        )

        self._last_rewards.append(erikas_reward)
        self._ctr += 1
        if self._ctr >= self._report_after:
            self._ctr -= self._report_after
            self.log.info(f"Last rewards: {self._last_rewards}")
            self._last_rewards = []

        return erikas_reward
