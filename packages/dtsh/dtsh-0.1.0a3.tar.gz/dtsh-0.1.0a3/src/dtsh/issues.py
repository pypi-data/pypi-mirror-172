# Copyright (c) 2022 Chris Duf <chris@openmarl.org>
#
# SPDX-License-Identifier: Apache-2.0

"""Find issues."""

import os
import sys

from devicetree.edtlib import EDT, Binding, ControllerAndData, Node, Property, PropertySpec

from dtsh.dtsh import DtshError


PropertyValueType = int | str | list[int] | list[str] | Node | list[Node] | list[ControllerAndData]


def run() -> None:
    dt_src_path = sys.argv[1] if len(sys.argv) > 1 else None
    dt_bindings_path = sys.argv[2:] if len(sys.argv) > 2 else None
    if not dt_bindings_path:
        zephyr_base = os.getenv('ZEPHYR_BASE')
        if zephyr_base:
            dt_bindings_path = [
                os.path.join(zephyr_base, 'boards'),
                os.path.join(zephyr_base, 'dts', 'bindings')
            ]
        else:
            raise DtshError('Please provide DT bindings or set ZEPHYR_BASE.')

    edt = EDT(dt_src_path, dt_bindings_path)
    _find_issues_node_attrs(edt)
    _find_issues_properties(edt)
    _find_issues_property_specs(edt)
    _find_issues_node_interrupts(edt)
    _find_issues_property_bindings(edt)


def _find_issues_node_attrs(edt: EDT) -> None:
    for node in edt.nodes:
        assert type(node) == Node
        assert hasattr(node, 'name')
        assert node.name is not None
        assert hasattr(node, 'unit_addr')
        assert hasattr(node, 'description')
        assert hasattr(node, 'path')
        assert node.path is not None
        assert hasattr(node, 'label')
        assert hasattr(node, 'labels')
        assert node.labels is not None
        assert hasattr(node, 'parent')
        assert hasattr(node, 'children')
        assert hasattr(node, 'dep_ordinal')
        assert node.dep_ordinal is not None
        assert hasattr(node, 'required_by')
        assert node.required_by is not None
        assert hasattr(node, 'depends_on')
        assert node.depends_on is not None
        assert hasattr(node, 'status')
        assert node.status is not None
        assert hasattr(node, 'read_only')
        assert node.read_only is not None
        assert hasattr(node, 'matching_compat')
        assert hasattr(node, 'binding_path')
        assert hasattr(node, 'compats')
        assert node.compats is not None
        assert hasattr(node, 'ranges')
        assert node.ranges is not None
        assert hasattr(node, 'regs')
        assert node.regs is not None
        assert hasattr(node, 'props')
        assert node.props is not None
        assert hasattr(node, 'aliases')
        assert node.aliases is not None
        assert hasattr(node, 'interrupts')
        assert node.interrupts is not None
        assert hasattr(node, 'pinctrls')
        assert node.pinctrls is not None
        assert hasattr(node, 'bus')
        assert hasattr(node, 'on_bus')
        assert hasattr(node, 'bus_node')
        assert hasattr(node, 'spi_cs_gpio')
# Issue: attempting to access Node.flash_controller attribute
# when the node does not have parent and grandparent will
# raise an EDTError.
#
# Returning None might be preferable ?
#
# ❯ python -m dtsh.issues $ZEPHYR_BASE/build/zephyr/zephyr.dts
# Traceback (most recent call last):
#   File "/usr/lib64/python3.10/runpy.py", line 196, in _run_module_as_main
#     return _run_code(code, main_globals, None,
#   File "/usr/lib64/python3.10/runpy.py", line 86, in _run_code
#     exec(code, run_globals)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 79, in <module>
#     run()
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 30, in run
#     _find_issues_node_attrs(edt)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 75, in _find_issues_node_attrs
#     assert hasattr(node, 'flash_controller')
#   File "/mnt/repos/github/dottspina/dtsh/.venv/lib64/python3.10/site-packages/devicetree/edtlib.py", line 803, in flash_controller
#     _err(f"flash partition {self!r} lacks parent or grandparent node")
#   File "/mnt/repos/github/dottspina/dtsh/.venv/lib64/python3.10/site-packages/devicetree/edtlib.py", line 2921, in _err
#     raise EDTError(msg)
# devicetree.edtlib.EDTError: flash partition <Node / in '/mnt/platform/zephyr-rtos/workspaces/zephyr-upstream/zephyr/build/zephyr/zephyr.dts', no binding> lacks parent or grandparent node
#
#assert hasattr(node, 'flash_controller')


def _find_issues_properties(edt: EDT) -> None:
    for node in edt.nodes:
        for prop_name in node.props:
            prop = node.props[prop_name]
            assert type(prop) == Property
            assert hasattr(prop, 'node')
            assert prop.node is not None
            assert hasattr(prop, 'spec')
            assert prop.spec is not None
            assert hasattr(prop, 'name')
            assert prop.name is not None
            assert hasattr(prop, 'type')
            assert prop.type is not None
            assert hasattr(prop, 'val')
            assert prop.val is not None
            assert hasattr(prop, 'enum_index')
# Issue: will call strip() on NoneType object when Property.spec.description
# is None.
#
# Traceback (most recent call last):
#   File "/usr/lib64/python3.10/runpy.py", line 196, in _run_module_as_main
#     return _run_code(code, main_globals, None,
#   File "/usr/lib64/python3.10/runpy.py", line 86, in _run_code
#     exec(code, run_globals)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 149, in <module>
#     run()
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 31, in run
#     _find_issues_properties(edt)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 139, in _find_issues_properties
#     assert prop.description is not None
#   File "/mnt/repos/github/dottspina/dtsh/.venv/lib64/python3.10/site-packages/devicetree/edtlib.py", line 1638, in description
#     return self.spec.description.strip()
# AttributeError: 'NoneType' object has no attribute 'strip'
#
# Known properties where Property.spec.description is None:
# + compatible
# + reg
# + status
# + gpios
# + pwms
#
# Property 'compatible' of node /
# Property 'compatible' of node /soc
# Property 'compatible' of node /soc/timer@e000e010
# Property 'reg' of node /soc/timer@e000e010
# Property 'status' of node /soc/timer@e000e010
# Property 'compatible' of node /leds
# Property 'gpios' of node /leds/led_0
# Property 'gpios' of node /leds/led_1
# Property 'gpios' of node /leds/led_2
# Property 'gpios' of node /leds/led_3
# Property 'compatible' of node /pwmleds
# Property 'pwms' of node /pwmleds/pwm_led_0
# Property 'gpios' of node /buttons/button_0
# Property 'gpios' of node /buttons/button_1
# Property 'gpios' of node /buttons/button_2
# Property 'gpios' of node /buttons/button_3
#
# Note: hasattr() is implemented by calling getattr(object, name)
# and seeing whether it raises an AttributeError or not.
# Seems that it will also return False when getattr() raises
# another type of exception.
#
#assert hasattr(prop, 'description')
            if not hasattr(prop, 'description'):
                print(f"None description: Property '{prop_name}' of node {prop.node.path}")


def _find_issues_property_specs(edt: EDT) -> None:
    for node in edt.nodes:
        for prop_name in node.props:
            prop = node.props[prop_name]
            if prop.spec is not None:
                spec = prop.spec
                assert type(spec) == PropertySpec
                assert hasattr(spec, 'binding')
                assert spec.binding is not None
                assert type(spec.binding) == Binding
                assert hasattr(spec, 'name')
                assert spec.name is not None
                assert hasattr(spec, 'path')
                assert hasattr(spec, 'type')
                assert spec.type is not None
                assert hasattr(spec, 'description')
                assert hasattr(spec, 'enum')
                assert hasattr(spec, 'const')
                assert hasattr(spec, 'default')
                assert hasattr(spec, 'deprecated')
                assert spec.deprecated is not None
                assert hasattr(spec, 'required')
                assert spec.required is not None
                assert hasattr(spec, 'specifier_space')
# Issue: Binding.path may be None, not stated in the Binding class docstring
#
# Known affected property specs: 'compatible', 'reg', 'status'
#
#assert spec.path is not None
                if spec.path is None:
                    print(f"None path: PropertySpec '{spec.name}' from binding {spec.binding.compatible}")
# Issue: Binding.description may be None, not stated in the Binding class docstring
#
# Known affected property specs: 'compatible', 'reg', 'status', 'gpios', 'pwms'
#
#assert spec.description is not None
                if spec.description is None:
                    print(f"None description: PropertySpec '{spec.name}' from binding {spec.binding.compatible}")


def _find_issues_property_bindings(edt: EDT) -> None:
    for node in edt.nodes:
        for prop_name in node.props:
            prop = node.props[prop_name]
            if prop.spec.binding:
                binding = prop.spec.binding
                assert hasattr(binding, 'path')
                assert hasattr(binding, 'compatible')
                assert hasattr(binding, 'prop2specs')
                assert binding.prop2specs is not None
                assert hasattr(binding, 'specifier2cells')
                assert binding.specifier2cells is not None
                assert hasattr(binding, 'raw')
                assert binding.raw is not None
                assert hasattr(binding, 'bus')
                assert hasattr(binding, 'on_bus')
                assert hasattr(binding, 'child_binding')
# Issue: Binding.path may be None, not stated in the Binding class docstring
#
# Known affected property bindings: 'compatible', 'reg', 'status'.
#
# This will also raise an error in Binding.__repr__():
# Traceback (most recent call last):
#   File "/usr/lib64/python3.10/runpy.py", line 196, in _run_module_as_main
#     return _run_code(code, main_globals, None,
#   File "/usr/lib64/python3.10/runpy.py", line 86, in _run_code
#     exec(code, run_globals)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 305, in <module>
#     run()
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 33, in run
#     _find_issues_property_bindings(edt)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 267, in _find_issues_property_bindings
#     print(f"description KeyError: {str(binding)}\n")
#   File "/mnt/repos/github/dottspina/dtsh/.venv/lib64/python3.10/site-packages/devicetree/edtlib.py", line 1797, in __repr__
#     return f"<Binding {os.path.basename(self.path)}" + compat + ">"
#   File "/usr/lib64/python3.10/posixpath.py", line 142, in basename
#     p = os.fspath(p)
# TypeError: expected str, bytes or os.PathLike object, not NoneType
#
#assert binding.path is not None
                if binding.path is None:
                    print(f"binding.path None: property spec {prop.spec.name}\n")
################################################################################
# Issue: Binding.description may be None, not stated in the Binding class docstring
#
#assert binding.description is not None
################################################################################
#
# Issue: attempting to access Binding.description may raise KeyError
# when the node does not have parent and grandparent will
# raise an EDTError.
#
# Known affected property bindings: 'compatible', 'reg', 'status'.
#
# Traceback (most recent call last):
#   File "/usr/lib64/python3.10/runpy.py", line 196, in _run_module_as_main
#     return _run_code(code, main_globals, None,
#   File "/usr/lib64/python3.10/runpy.py", line 86, in _run_code
#     exec(code, run_globals)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 268, in <module>
#     run()
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 33, in run
#     _find_issues_property_bindings(edt)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 221, in _find_issues_property_bindings
#     assert hasattr(binding, 'description')
#   File "/mnt/repos/github/dottspina/dtsh/.venv/lib64/python3.10/site-packages/devicetree/edtlib.py", line 1802, in description
#     return self.raw['description']
# KeyError: 'description'
#
#assert hasattr(binding, 'description')
                try:
                    hasattr(binding, 'description')
                except KeyError:
                    print(f"description KeyError: {prop.spec.name} for node {prop.node.path}\n")


def _find_issues_node_interrupts(edt: EDT) -> None:
    for node in edt.nodes:
        for irq in node.interrupts:
            assert type(irq) == ControllerAndData
            assert hasattr(irq, 'node')
            assert irq.node is not None
            assert hasattr(irq, 'controller')
            assert irq.controller is not None
            assert hasattr(irq, 'data')
            assert irq.data is not None
            assert hasattr(irq, 'name')
# Issue: ControllerAndData.basename undefined for node interrupts
#
# See:
# - Node.interrupts
# - Node._init_interrupts(().
#
# Traceback (most recent call last):
#   File "/usr/lib64/python3.10/runpy.py", line 196, in _run_module_as_main
#     return _run_code(code, main_globals, None,
#   File "/usr/lib64/python3.10/runpy.py", line 86, in _run_code
#     exec(code, run_globals)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 224, in <module>
#     run()
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 32, in run
#     _find_issues_node_interrupts(edt)
#   File "/mnt/repos/github/dottspina/dtsh/src/dtsh/issues.py", line 217, in _find_issues_node_interrupts
#     irq.basename
# AttributeError: 'ControllerAndData' object has no attribute 'basename'
#
#assert hasattr(irq, 'basename')
            if not hasattr(irq, 'basename'):
                print(f"No basename: IRQ for node {irq.node.name}, ctrl {irq.controller.name}")


if __name__ == "__main__":
    run()
