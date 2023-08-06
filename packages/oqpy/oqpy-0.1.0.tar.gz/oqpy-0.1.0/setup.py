# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oqpy']

package_data = \
{'': ['*']}

install_requires = \
['mypy-extensions>=0.4.3,<0.5.0', 'numpy==1.21.6', 'openpulse==0.4.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'oqpy',
    'version': '0.1.0',
    'description': 'Generating OpenQASM 3 + OpenPulse in Python',
    'long_description': '# OQpy: Generating OpenQASM 3 + OpenPulse in Python\n\nThe goal of `oqpy` ("ock-pie") is to make it easy to generate OpenQASM 3 + OpenPulse in Python. The\n`oqpy` library builds off of the [`openqasm3`][openqasm3] and [`openpulse`][openpulse] packages,\nwhich serve as Python reference implementations of the _abstract syntax tree_ (AST) for the\nOpenQASM 3 and OpenPulse grammars.\n\n[openqasm3]: https://pypi.org/project/openqasm3/\n[openpulse]: https://pypi.org/project/openpulse/\n\n## What are OpenQASM 3 and OpenPulse?\n\nOpenQASM is an imperative programming language designed for near-term quantum computing algorithms\nand applications. [OpenQASM 3][openqasm3-docs] extends the original specification by adding support\nfor classical logic, explicit timing, and pulse-level definitions. The latter is enabled via the use\nof [_calibration grammars_][pulse-docs] which allow quantum hardware builders to extend the language\nto support hardware-specific directives via `cal` and `defcal` blocks. One such grammar is\n[OpenPulse][openpulse-docs], which provides the instructions required for pulse-based control of\nmany common quantum computing architectures (e.g. superconducting qubits).\n\n[openqasm3-docs]: https://openqasm.com/\n[pulses-docs]: https://openqasm.com/language/pulses.html\n[openpulse-docs]: https://openqasm.com/language/openpulse.html\n\n## Installation and Getting Started\n\nOQpy can be installed from [PyPI][pypi] or from source in an environment with Python 3.7 or greater.\n\nTo install it from PyPI (via `pip`), do the following:\n\n```\npip install oqpy\n```\n\nTo instead install OQpy from source, do the following from within the repository after cloning it:\n\n```\npoetry install\n```\n\nNext, check out the following example to get a sense of the kinds of programs we can write with\nOQpy.\n\n[pypi]: https://pypi.org/project/oqpy/\n\n## Example: Ramsey Interferometry\n\nA common and useful experiment for qubit characterization is [Ramsey interferometry][ramsey],\nwhich can be used for two purposes: performing a careful measurement of a qubit’s resonant\nfrequency, and for investigating how long a qubit retains its coherence. In a typical Ramsey\nexperiment, one varies the length of a delay between the two π/2 pulses, and then measures the state\nof the qubit. Below, we\'ll create a Ramsey interferometry experiment in OpenQASM 3 using OQpy.\nAs part of this, we’ll use the OpenPulse grammar to allow this experiment to specify its operation\nimplementations at the calibrated pulse level.\n\n[ramsey]: https://en.wikipedia.org/wiki/Ramsey_interferometry\n\n```python\nimport oqpy\nprog = oqpy.Program()  # create a new oqpy program\n\n# Declare frames: transmon driving frame and readout receive/transmit frames\nxy_frame = oqpy.FrameVar(oqpy.PortVar("dac0"), 6.431e9, name="xy_frame")\nrx_frame = oqpy.FrameVar(oqpy.PortVar("adc0"), 5.752e9, name="rx_frame")\ntx_frame = oqpy.FrameVar(oqpy.PortVar("dac1"), 5.752e9, name="tx_frame")\n\n# Declare the type of waveform we are working with\nconstant_waveform = oqpy.declare_waveform_generator(\n    "constant",\n    [("length", oqpy.duration),\n     ("amplitude", oqpy.float64)],\n)\ngaussian_waveform = oqpy.declare_waveform_generator(\n    "gaussian",\n    [("length", oqpy.duration),\n     ("sigma", oqpy.duration),\n     ("amplitude", oqpy.float64)],\n)\n\n# Provide gate / operation definitions as defcals\nqubit = oqpy.PhysicalQubits[1]  # get physical qubit 1\n\nwith oqpy.defcal(prog, qubit, "reset"):\n    prog.delay(1e-3)  # reset to ground state by waiting 1 ms\n\nwith oqpy.defcal(prog, qubit, "measure"):\n    prog.play(tx_frame, constant_waveform(2.4e-6, 0.2))\n    prog.capture(rx_frame, constant_waveform(2.4e-6, 1))\n\nwith oqpy.defcal(prog, qubit, "x90"):\n    prog.play(xy_frame, gaussian_waveform(32e-9, 8e-9, 0.2063))\n\n# Loop over shots (i.e. repetitions)\ndelay_time = oqpy.DurationVar(0, "delay_time")  # initialize a duration\nwith oqpy.ForIn(prog, range(100), "shot_index"):\n    prog.set(delay_time, 0)                     # reset delay time to zero\n    # Loop over delays\n    with oqpy.ForIn(prog, range(101), "delay_index"):\n        (prog.reset(qubit)                      # prepare in ground state\n         .gate(qubit, "x90")                    # pi/2 pulse (90° rotation about the x-axis)\n         .delay(delay_time, qubit)              # variable delay\n         .gate(qubit, "x90")                    # pi/2 pulse (90° rotation about the x-axis)\n         .measure(qubit)                        # final measurement\n         .increment(delay_time, 100e-9))        # increase delay by 100 ns\n```\n\nRunning `print(prog.to_qasm(encal_declarations=True))` generates the following OpenQASM:\n\n```qasm3\nOPENQASM 3.0;\ndefcalgrammar "openpulse";\ncal {\n    extern constant(duration, float[64]) -> waveform;\n    extern gaussian(duration, duration, float[64]) -> waveform;\n    port dac1;\n    port adc0;\n    port dac0;\n    frame tx_frame = newframe(dac1, 5752000000.0, 0);\n    frame rx_frame = newframe(adc0, 5752000000.0, 0);\n    frame xy_frame = newframe(dac0, 6431000000.0, 0);\n}\nduration delay_time = 0.0ns;\ndefcal reset $1 {\n    delay[1000000.0ns];\n}\ndefcal measure $1 {\n    play(tx_frame, constant(2400.0ns, 0.2));\n    capture(rx_frame, constant(2400.0ns, 1));\n}\ndefcal x90 $1 {\n    play(xy_frame, gaussian(32.0ns, 8.0ns, 0.2063));\n}\nfor int shot_index in [0:99] {\n    delay_time = 0.0ns;\n    for int delay_index in [0:100] {\n        reset $1;\n        x90 $1;\n        delay[delay_time] $1;\n        x90 $1;\n        measure $1;\n        delay_time += 100.0ns;\n    }\n}\n```\n\n## Contributing\n\nWe welcome contributions to OQpy including bug fixes, feature requests, etc. To get started, check\nout our [contributing guidelines](CONTRIBUTING.md).\n',
    'author': 'OQpy Contributors',
    'author_email': 'oqpy-contributors@amazon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/openqasm/oqpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
