#  Copyright (c) 2015-2018 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import os
from typing import Optional

import pytest
from pytest import FixtureRequest

from molecule.test.functional.conftest import (
    idempotence,
    init_role,
    init_scenario,
    list_with_format_plain,
    run_test,
    verify,
)
from molecule.util import run_command


@pytest.fixture
def scenario_to_test(request):
    return request.param


@pytest.fixture
def scenario_name(request):
    try:
        return request.param
    except AttributeError:
        return None


@pytest.fixture
def driver_name(request: FixtureRequest) -> Optional[str]:
    try:
        # https://stackoverflow.com/q/65334215/99834
        return request.param  # type: ignore
    except AttributeError:
        return None


@pytest.fixture
def platform_name(request):
    try:
        return request.param
    except AttributeError:
        return None


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_check(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "check", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
@pytest.mark.serial
def test_command_cleanup(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "cleanup", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
@pytest.mark.serial
def test_command_converge(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "converge", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
@pytest.mark.serial
def test_command_create(scenario_to_test, with_scenario, scenario_name, tmp_path):
    cmd = ["molecule", "create", "--scenario-name", scenario_name]
    assert run_command(cmd, env=os.environ).returncode == 0

    # TODO(ssbarnea): Include these additional checks
    # role_list = run_command(["ansible-galaxy", "role", "list"], env=os.environ)
    # assert role_list.returncode == 0, role_list
    # assert "- molecule.delegated_test, (unknown version)" in role_list.stdout


@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        pytest.param(
            "dependency",
            "delegated",
            "shell",
            id="shell",
        ),
        pytest.param(
            "dependency",
            "delegated",
            "ansible-galaxy",
            id="galaxy",
        ),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
@pytest.mark.serial
def test_command_dependency(request, scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "dependency", "--scenario-name", scenario_name]
    assert run_command(cmd, echo=True).returncode == 0

    # Validate that dependency worked by running converge, which make use
    cmd = ["molecule", "converge", "--scenario-name", scenario_name]
    assert run_command(cmd, echo=True).returncode == 0


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [("driver/delegated", "delegated", "default")],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_destroy(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "destroy", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_idempotence(scenario_to_test, with_scenario, scenario_name):
    idempotence(scenario_name)


@pytest.mark.serial
@pytest.mark.parametrize("driver_name", [("delegated")], indirect=["driver_name"])
def test_command_init_role(temp_dir, driver_name):
    init_role(temp_dir, driver_name)


@pytest.mark.serial
@pytest.mark.parametrize("driver_name", [("delegated")], indirect=["driver_name"])
def test_command_init_scenario(temp_dir, driver_name):
    init_scenario(temp_dir, driver_name)


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_lint(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "lint", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, expected",
    [
        (
            "driver/delegated",
            "delegated",
            "instance        delegated       ansible default",
        ),
    ],
    indirect=["scenario_to_test", "driver_name"],
)
def test_command_list_with_format_plain(scenario_to_test, with_scenario, expected):
    list_with_format_plain(expected)


# @pytest.mark.parametrize(
#     "scenario_to_test, driver_name, login_args, scenario_name",
#     [
#         (
#             "driver/delegated",
#             "delegated",
#             [["instance", ".*instance.*"]],
#             "default",
#         ),
#     ],
#     indirect=["scenario_to_test", "driver_name", "scenario_name"],
# )
# def test_command_login(scenario_to_test, with_scenario, login_args, scenario_name):
#     login(login_args, scenario_name)


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_prepare(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "create", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0

    cmd = ["molecule", "prepare", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_side_effect(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "side-effect", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_syntax(scenario_to_test, with_scenario, scenario_name):
    cmd = ["molecule", "syntax", "--scenario-name", scenario_name]
    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_test(scenario_to_test, with_scenario, scenario_name, driver_name):
    run_test(driver_name, scenario_name)


def run_test_with_platform_name(
    driver_name, platform_name, scenario_name="default", parallel=False
):
    cmd = [
        "molecule",
        "-vvv",
        "--debug",
        "test",
        "--scenario-name",
        scenario_name,
        "--platform-name",
        platform_name,
    ]
    if driver_name != "delegated":
        if scenario_name is None:
            cmd.append("--all")
        if parallel:
            cmd.append("--parallel")

    assert run_command(cmd).returncode == 0


@pytest.mark.serial
@pytest.mark.parametrize(
    ("scenario_to_test", "driver_name", "scenario_name", "platform_name"),
    [
        ("driver/delegated", "delegated", "default", "instance"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name", "platform_name"],
)
def test_command_test_with_platform_name(
    scenario_to_test, with_scenario, scenario_name, driver_name, platform_name
):
    run_test_with_platform_name(driver_name, platform_name, scenario_name)


@pytest.mark.serial
@pytest.mark.parametrize(
    ("scenario_to_test", "driver_name", "scenario_name"),
    [
        (
            "driver/delegated_invalid_role_name_with_role_name_check_equals_to_1",
            "delegated",
            "default",
        ),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_test_with_role_name_check_equals_to_1(
    scenario_to_test, with_scenario, scenario_name, driver_name
):
    run_test(driver_name, scenario_name)


@pytest.mark.serial
@pytest.mark.extensive
@pytest.mark.parametrize(
    "scenario_to_test, driver_name, scenario_name",
    [
        ("driver/delegated", "delegated", "default"),
    ],
    indirect=["scenario_to_test", "driver_name", "scenario_name"],
)
def test_command_verify(scenario_to_test, with_scenario, scenario_name):
    verify(scenario_name)


def test_sample_collection():
    assert (
        run_command(
            ["molecule", "test"], cwd="src/molecule/test/resources/sample-collection"
        ).returncode
        == 0
    )
