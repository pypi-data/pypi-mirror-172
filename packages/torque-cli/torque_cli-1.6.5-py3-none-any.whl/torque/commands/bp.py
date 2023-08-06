import logging
from typing import Any

from torque.branch.branch_context import ContextBranch
from torque.branch.branch_utils import get_and_check_folder_based_repo
from torque.commands.base import BaseCommand
from torque.models.blueprints import BlueprintsManager
from torque.parsers.command_input_validators import CommandInputValidator

logger = logging.getLogger(__name__)


class BlueprintsCommand(BaseCommand):
    """
    usage:
        torque (bp | blueprint) list [--output=json | --output=json --detail]
        torque (bp | blueprint) get <name> [--source=<source_type>] [--output=json | --output=json --detail]
        torque (bp | blueprint) [--help]

    options:
       -o --output=json           Yield output in JSON format

       -s --source=<source_type>  Specify a type of blueprint source: 'torque' or 'git'. [default: git]

       -d --detail                Obtain full blueprint data in JSON format

       -h --help                  Show this message
    """

    RESOURCE_MANAGER = BlueprintsManager

    def get_actions_table(self) -> dict:
        return {
            "list": self.do_list,
            # "validate": self.do_validate,
            "get": self.do_get,
        }

    def do_list(self) -> (bool, Any):
        detail = self.input_parser.blueprint_list.detail
        try:
            if detail:
                blueprint_list = self.manager.list_detailed()
            else:
                blueprint_list = self.manager.list()
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die()

        return True, blueprint_list

    def do_get(self) -> (bool, Any):
        detail = self.input_parser.blueprint_get.detail
        blueprint_name = self.input_parser.blueprint_get.blueprint_name
        source = self.input_parser.blueprint_get.source

        try:
            if detail:
                bp = self.manager.get_detailed(blueprint_name, source)
            else:
                bp = self.manager.get(blueprint_name, source)
        except Exception as e:
            logger.exception(e, exc_info=False)
            return self.die(f"Unable to get details of blueprint '{blueprint_name}'")

        return True, bp

    def do_validate(self) -> (bool, Any):
        blueprint_name = self.input_parser.blueprint_validate.blueprint_name
        branch = self.input_parser.blueprint_validate.branch
        commit = self.input_parser.blueprint_validate.commit

        CommandInputValidator.validate_commit_and_branch_specified(branch, commit)

        repo = get_and_check_folder_based_repo(blueprint_name)
        with ContextBranch(repo, branch) as context_branch:
            if not context_branch:
                return self.error("Unable to Validate BP")
            try:
                bp = self.manager.validate(
                    blueprint=blueprint_name, branch=context_branch.validation_branch, commit=commit
                )
            except Exception as e:
                logger.exception(e, exc_info=False)
                return self.die()

        errors = getattr(bp, "errors")

        if errors:
            logger.info("Blueprint validation failed")
            return self.die(errors)

        else:
            return self.success("Blueprint is valid")
