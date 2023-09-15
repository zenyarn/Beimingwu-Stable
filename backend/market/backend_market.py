import os
import copy
from shutil import copyfile, rmtree
import zipfile
import torch
import numpy as np
import pandas as pd
from cvxopt import solvers, matrix
from typing import Tuple, Any, List, Union, Dict
import werkzeug.datastructures

from learnware.market import EasyMarket

from learnware.learnware import Learnware, get_learnware_from_dirpath
from learnware.logger import get_module_logger
import traceback


logger = get_module_logger("market", "INFO")


class BackendMarket(EasyMarket):
    """Backend Market is deadicated to the backend service"""

    INVALID_LEARNWARE = -1
    NONUSABLE_LEARNWARE = 0
    USABLE_LEARWARE = 1

    def __init__(self, market_id: str = "default", rebuild: bool = False):
        """Initialize Learnware Market.
        Automatically reload from db if available.
        Build an empty db otherwise.

        Parameters
        ----------
        market_id : str, optional, by default 'default'
            The unique market id for market database

        rebuild : bool, optional
            Clear current database if set to True, by default False
            !!! Do NOT set to True unless highly necessary !!!
        """
        super().__init__(market_id, rebuild)

    def add_learnware(self, zip_path: str, semantic_spec: dict, learnware_id: str = None) -> Tuple[str, bool]:
        """Add a learnware into the market.

        .. note::

            Given a prediction of a certain time, all signals before this time will be prepared well.


        Parameters
        ----------
        zip_path : str
            Filepath for learnware model, a zipped file.
        semantic_spec : dict
            semantic_spec for new learnware, in dictionary format.

        Returns
        -------
        Tuple[str, int]
            - str indicating model_id
            - int indicating what the flag of learnware is added.

        """
        semantic_spec = copy.deepcopy(semantic_spec)

        if not os.path.exists(zip_path):
            logger.warning("Zip Path NOT Found! Fail to add learnware.")
            return None, self.INVALID_LEARNWARE

        try:
            if len(semantic_spec["Data"]["Values"]) == 0:
                logger.warning("Illegal semantic specification, please choose Data.")
                return None, self.INVALID_LEARNWARE
            if len(semantic_spec["Task"]["Values"]) == 0:
                logger.warning("Illegal semantic specification, please choose Task.")
                return None, self.INVALID_LEARNWARE
            if len(semantic_spec["Library"]["Values"]) == 0:
                logger.warning("Illegal semantic specification, please choose Device.")
                return None, self.INVALID_LEARNWARE
            if len(semantic_spec["Name"]["Values"]) == 0:
                logger.warning("Illegal semantic specification, please provide Name.")
                return None, self.INVALID_LEARNWARE
            if len(semantic_spec["Description"]["Values"]) == 0 and len(semantic_spec["Scenario"]["Values"]) == 0:
                logger.warning("Illegal semantic specification, please provide Scenario or Description.")
                return None, self.INVALID_LEARNWARE
            if (
                semantic_spec["Data"]["Type"] != "Class"
                or semantic_spec["Task"]["Type"] != "Class"
                or semantic_spec["Library"]["Type"] != "Class"
                or semantic_spec["Scenario"]["Type"] != "Tag"
                or semantic_spec["Name"]["Type"] != "String"
                or semantic_spec["Description"]["Type"] != "String"
            ):
                logger.warning("Illegal semantic specification, please provide the right type.")
                return None, self.INVALID_LEARNWARE
        except:
            print(semantic_spec)
            logger.warning("Illegal semantic specification, some keys are missing.")
            return None, self.INVALID_LEARNWARE

        logger.info("Get new learnware from %s" % (zip_path))
        if learnware_id is not None:
            id = learnware_id
        else:
            id = "%08d" % (self.count)
        target_zip_dir = os.path.join(self.learnware_zip_pool_path, "%s.zip" % (id))
        target_folder_dir = os.path.join(self.learnware_folder_pool_path, id)
        copyfile(zip_path, target_zip_dir)

        with zipfile.ZipFile(target_zip_dir, "r") as z_file:
            z_file.extractall(target_folder_dir)
        logger.info("Learnware move to %s, and unzip to %s" % (target_zip_dir, target_folder_dir))

        try:
            new_learnware = get_learnware_from_dirpath(
                id=id, semantic_spec=semantic_spec, learnware_dirpath=target_folder_dir
            )
        except:
            try:
                os.remove(target_zip_dir)
                rmtree(target_folder_dir)
            except:
                pass
            return None, self.INVALID_LEARNWARE

        if new_learnware is None:
            return None, self.INVALID_LEARNWARE

        self.dbops.add_learnware(
            id=id,
            semantic_spec=semantic_spec,
            zip_path=target_zip_dir,
            folder_path=target_folder_dir,
            use_flag=EasyMarket.USABLE_LEARWARE,
        )

        self.learnware_list[id] = new_learnware
        self.learnware_zip_list[id] = target_zip_dir
        self.learnware_folder_list[id] = target_folder_dir
        self.count += 1
        return id, EasyMarket.USABLE_LEARWARE

    def update_learnware(
        self, id: str, semantic_specification: dict, learnware_file: werkzeug.datastructures.FileStorage = None
    ):
        self.dbops.update_learnware_semantic_specification(id, semantic_specification)

        if learnware_file is not None:
            zip_path = self.learnware_zip_list[id]
            folder_path = self.learnware_folder_list[id]

            learnware_file.save(zip_path)
            with zipfile.ZipFile(zip_path, "r") as z_file:
                z_file.extractall(folder_path)
                pass
            self.learnware_list[id] = get_learnware_from_dirpath(
                id=id, semantic_spec=semantic_specification, learnware_dirpath=folder_path
            )
        else:
            self.learnware_list[id].get_specification().update_semantic_spec(semantic_specification)
        pass

    def get_all_learnware(
        self,
    ) -> List[Learnware]:
        return self.learnware_list.values()
