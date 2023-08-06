Welcome to _BatchX' python toolbox_, or _"the toolbox"_ for short.
The toolbox makes the life of BatchX (python) developers **more pleasant**.
To do so, it provides tools that help devs to work more effectively.


# Table of Contents
- [Installation](https://github.com/batchx/python-toolbox#installation)
    - [Local](https://github.com/batchx/python-toolbox#local)
    - [Inside Docker image](https://github.com/batchx/python-toolbox#inside-docker-image)
- [The manifest as single source of truth](https://github.com/batchx/python-toolbox#the-manifest-as-single-source-of-truth)
- [`bx-readme`](https://github.com/batchx/python-toolbox#bx-readme)
- [CommandBuilder](https://github.com/batchx/python-toolbox#commandbuilder)
    - [Connecting CLI parameters to BatchX parameters](https://github.com/batchx/python-toolbox#connecting-tool-parameters-to-batchx-parameters)
    - [Understanding parameter types](https://github.com/batchx/python-toolbox#understanding-parameter-types)
    - [Add action](https://github.com/batchx/python-toolbox#add-actions)
    - [Specify constraints](https://github.com/batchx/python-toolbox#specify-constraints)
    



# Installation

The toolbox is available on [PyPi](https://pypi.org/project/batchx-dev/).

## Local

Simple: do a `pip install`

```shell
python -m pip install batchx-dev
```

For reproducibility, it often makes sense to 'lock' yourself into a specific version.
This can be done as follows:
```shell
python -m pip install batchx-dev==1.0.63
```

## Inside Docker image

Installation of the toolbox inside the docker image of a BatchX tool is _almost_ identical to a local install, except for the fact that the `pip install` command now has to be part of the Dockerfile.
For the sake of argument, we assume that you are working on bringing a bioinformatics tool called `biotool` into BatchX, and that your directory structure looks like this,
```
biotool
├── Dockerfile
├── run_biotool.py
└── manifest
    ├── manifest.json
    ├── picture.png
    └── readme.md
```

Suppose that, initially, `biotool/Dockerfile` looked as follows;

```dockerfile
FROM amd64/python:3.10.4-bullseye

RUN python -m pip install biotool==2.4.2

RUN mkdir batchx
RUN chmod -R 777 /batchx

COPY run_biotool.py /batchx
ENTRYPOINT python /batchx/run_biotool.py

LABEL io.batchx.manifest=10
COPY manifest /batchx/manifest
```

installation of the toolbox inside the image requires the addition of a single line,

```dockerfile
RUN python -m pip install batchx-dev==1.0.63
```

which yields a `Dockerfile` that looks like this:

```dockerfile
FROM amd64/python:3.10.4-bullseye

RUN python -m pip install batchx-dev==1.0.63

RUN python -m pip install biotool==2.4.2

RUN mkdir batchx
RUN chmod -R 777 /batchx

COPY run_biotool.py /batchx
ENTRYPOINT python /batchx/run_biotool.py

LABEL io.batchx.manifest=10
COPY manifest /batchx/manifest
```

That's it.

Note that, in a Dockerfile, **you really should 'pin' a specific version of the packages you install**. 
If you do not do so, the Docker image may differ depending on when it was last built. 

# The manifest as single source of truth

Ultimately, the manifest is of utmost importance in BatchX.
On an abstract level, much of what the toolbox achieves comes down to making your code understand the manifest properly. 
Therefore, much of the explanations below are example-driven, showcasing different scenarios in which a manifest needs proper interpretation.


# `bx-readme`

The toolbox comes with a **`bx-readme` command** that helps to keep the `manifest.json` and the `readme.md` in sync.
We assume the following directory structure,
```
biotool
├── Dockerfile
├── run_biotool.py
└── manifest
    ├── manifest.json
    ├── picture.png
    └── readme.md
└── python-toolbox
    ├── manifest.json
    ├── ...
```

The manifest (i.e. `manifest/manifest.json`) is the [single source of truth](#the-manifest-as-single-source-of-truth), but the human-readable readme (i.e. `manifest/readme.md`) repeats a lot of that information.
As a consequence, changes in the manifest need to be reflected in the readme and vice-versa. 
This synchronisation process is prone to human error, which is why the toolbox steps in.

## Quickstart

Ensure that your terminal is in the `/manifest` directory (`cd manifest`), and do,
```shell
bx-readme
```
This will likely do what you want.
This command looks at `manifest.json` and `readme.md` and does its best to improve both.


### In-depth explanation
Run
```shell
bx-readme --help
```
for the latest information on the CLI.

Additionally, it is interesting to know that the `bx-readme` command internally relies on two objects:
- the `ManifestImprover` and
- the `ReadmeImprover`.

Those objects are responsible for exactly what their names suggest. 
The `bx-readme` command is nothing more than a single script that initializes those objects, configures them, runs them and saves the results.

However, much more is possible beyond the "one size fits all approach" of that particular script.
To get an idea of all the possibilities, the best reference is to study their respective integration tests.
- [ManifestImprover integration test](test/mf-improver.ipynb)
- [ReadmeImprover integration test](test/rm-improver.ipynb)
- [ManifestImprover-ReadmeImprover end-to-end integration test](test/mfi-rmi-end-to-end.ipynb)
        
        
# CommandBuilder

Apart from `bx-readme`, this toolbox also comes in handy when incorporating a bioinformatics tool into [batchx.io](https://www.batchx.io/).
In this section, we highlight some of its functionalities in that regard.

## Initialize the CommandBuilder

The `CommandBuilder` relies on a few additional datastructures, namely `Manifest` and `Filesystem` objects.

```python
from batchx_dev.toolbox import FileSystem, Manifest, CommandBuilder

fs = FileSystem(tool="biotool") # data-structure (approximately a dict) capturing the internal directory structure of a tool's docker image.
mf = Manifest(fs.mfp)  # load manifest.json

cb = CommandBuilder(mf, tool="biotool", filesystem=fs) # Initialize the CommandBuilder
```

## Connecting CLI parameters to BatchX parameters

Suppose the `biotool` CLI has an optional parameter `--maximum-length`
```shell
biotool --input genome.fasta --maximum-length 1000
```

which appears in the manifest as follows,
```json
"maximumLength": {
    "type": "integer",
    "required": false,
    "default": 250,
    "description": "Maximum length (in bp) for which biotool makes sense."
},
```

Obviously, the `biotool` parameter (`--maximum-length`) has a different name than the BatchX parameter (`maximumLength`).
But, in order to pass the user-provided value for this parameter from BatchX (CLI or web interface) into the underlying `biotool` CLI, this _obvious and trivial_ knowledge still needs to be represented _explicitly_ somewhere in the wrapper script `run_biotool.py`. 

This leads to code that looks like this, 
```python
maximum_length = parsed_json["maximumLength"]

...

command = "biotool "
if maximum_length is not None:
    command += "--maximum_length {}".format(maximum_length)
```

which is _not wrong_, but this is a lot of code _just_ to link `maximum_length` and `maximumLength` together.
In particular, note that this 
- parses a json;
- looks up the user-provided value of the parameter of interest (`maximumLength`);
- creates a new python variable (`maximum_length`) to house that value;
- checks if that variable has an _actual_ value (i.e. `is not None`);
- if yes:
    - creates a substring `--maximum_length`;
    - injects the value of your python variable `maximum_length` into that string;
    - and finally, extends the command string with this substring.

Whereas the only thing you _really had to do_ was to explain to your computer that `maximumLength` is a synonym for `--maximum_length` in this context.
Here, however, linking  `maximumLength` and `--maximum_length` gets intertwined with value-passing and actual command-generation.

Mixing all of this is suboptimal, because value-passing and actual command-generation of the `biotool` CLI command is something that needs to happen anyway, for any parameter:
that part is perfectly suitable for automation.
The linking together is _the only thing_ that requires actual human intervention here.

The toolbox allows you to do just that:
```python
cb.add_command(cmd="maximum_length", key="maximumLength")
```
The commandbuilder now knows that `maximumLength` is a synonym for `maximum_length`, and upon command generation will do what it needs to do.

### Example: Tool parameters to BatchX parameters

To illustrate, given this `input.json`,
```json
"fasta": "some_genome.fasta",
"maximumLength": 200
```
this `run_biotool.py` implementation
```python
from batchx_dev.toolbox import FileSystem, Manifest, CommandBuilder

fs = FileSystem(tool="biotool") # data-structure (approximately a dict) capturing the internal directory structure of a tool's docker image.
mf = Manifest(fs.mfp)  # load manifest.json (mfp = manifest filepath)
ip = Input(fs.ifp) # load input.json (ifp = input filepath)

cb = CommandBuilder(mf, tool="biotool", filesystem=fs) # Initialize the CommandBuilder

cb.add_command(cmd="input", key="fasta")
cb.add_command(cmd="maximum_length", key="maximumLength")

cb.build_command(ip)
```
yields the following command:
```shell
biotool --input some_genome.fasta --maximum-length 200
```

## Understanding parameter types

Suppose the `biotool` CLI has an optional _flag_ `--no-qc`, which allows users to run `biotool` without its built-in quality control mechanism,
forcing it to produce more but potentially less relevant outputs.
Since it is a _flag_, its mere presence indicates that this option is active. 
That is, this command
```shell
biotool --input genome.fasta --maximum-length 1000 --no-qc
```
runs `biotool` with quality control _disabled_, whereas this command
```shell
biotool --input genome.fasta --maximum-length 1000
```
runs `biotool` with quality control _enabled_.
Note the difference with "regular" command line _arguments_ (i.e. "key-value style"), such as `--input`  and `--maximum-length` that have to be followed by an actual value;
in flags, the value is implicit.

In a BatchX manifest, this flag can be described as follows,
```json
"noQC": {
    "type": "bool",
    "required": false,
    "default": false,
    "description": "Flag that indicates whether or not biotool's internal quality control mechanism should be bypassed."
},
```

Apart from linking the `biotool` parameter (`--no-qc`) and the BatchX parameter (`noQC`), developers now must also encode particular logic to inject this parameter's value into the final command, i.e.:
- if `noQC==True`, the flag must be present, 
- if `noQC==False` nothing needs to be added.

Obviously, this differs from how a command is built for regular (key-value style) arguments, which leads to code that looks like this, 
```python
maximum_length = parsed_json["maximumLength"]
no_qc = parsed_json["noQC"]

...

command = "biotool "
if maximum_length is not None:
    command += "--maximum_length {}".format(maximum_length)
if no_qc:
    command += "--no_qc"
```
again, nothing inherently wrong about this, but this intertwines proper understanding of the manifest and the parsing of the actual input. 
Another disadvantage is the fact that _readers_ of this code need to pay very close attention to figure out which parameters are _flags_ and which are _key-value_.

The toolbox, on the other hand, simply allows you to _explicitly_ state that a particular parameter is a flag,
```python
cb.add_command(cmd="maximum_length", key="maximumLength")
cb.add_command(cmd="no-qc", key="noQC").set_kind(kind="flag")
```
The commandbuilder now knows that `noQC` is a flag (and so do readers of this code!), and takes this into account when generating commands.

### Example: Understanding parameter types

To illustrate, given this `input.json`,
```json
"fasta": "some_genome.fasta",
"maximumLength": 200,
"noQC": true
```
this `run_biotool.py` implementation
```python
from batchx_dev.toolbox import FileSystem, Manifest, CommandBuilder

fs = FileSystem(tool="biotool") # data-structure (approximately a dict) capturing the internal directory structure of a tool's docker image.
ip = Input(fs.ifp) # load input.json
mf = Manifest(fs.mfp)  # load manifest.json

cb = CommandBuilder(mf, tool="biotool", filesystem=fs) # Initialize the CommandBuilder

cb.add_command(cmd="input", key="fasta")
cb.add_command(cmd="maximum_length", key="maximumLength")
cb.add_command(cmd="no-qc", key="noQC").set_kind(kind="flag")

cb.build_command(ip)
```
yields the following command:
```shell
biotool --input some_genome.fasta --maximum-length 200 --no-qc
```
whereas given this `input.json`,
```json
"fasta": "some_genome.fasta",
"maximumLength": 200,
"noQC": false
```
it generates this command instead:
```shell
biotool --input some_genome.fasta --maximum-length 200
```

## Add actions


### Example: Attaching an action to a parameter
To illustrate, given this `input.json`,
```json
"fasta": "some_genome.fasta.gz",
"maximumLength": 2000,
"noQC": true
```
this `run_biotool.py` implementation
```python
from batchx_dev.toolbox import FileSystem, Manifest, CommandBuilder

# define a useful function
def conditional_unzip_gzip(input, manifest, fp):
    """
    For constraints & actions:
        - First argument is always the Input object.
        - Second argument is always the Manifest object.
        - Third argument is always the value of the command with which the constraint is associated.
    """

    def is_gz_file(fp: str | Path):
        with open(fp, "rb") as f:
            return f.read(2) == b"\x1f\x8b"

    def unzip_gzip(gzip_fp, unzip_fp=None):
        """Unzips a gzipped file with pgiz."""
        gzip_fp = Path(gzip_fp)
        assert gzip_fp.suffix == ".gz", "Not the expected `.gz` extension!"

        if unzip_fp is None:
            unzip_fp = gzip_fp.parent / gzip_fp.stem  # removes .gz suffix

        print("Extracting target file {} using pigz".format(gzip_fp), flush=True)
        with open(unzip_fp, "w") as f:
            pigz = subprocess.call(["pigz", "-dc", str(gzip_fp)], stdout=f)
            if pigz != 0:
                sys.exit(pigz)
        return unzip_fp

    fp = Path(fp)
    if fp.suffix == ".gz":
        if is_gz_file(fp):
            return unzip_gzip(fp)
        else:
            msg = """
            Assumed that file {f} is gzipped.

            However, upon closer inspection (via `is_gz_file`),
            it turns out this is not the case. 

            Please resolve this issue.
            """.format(
                f=str(fp)
            )
            raise ValueError(msg)
    else:
        return fp

fs = FileSystem(tool="biotool") # data-structure (approximately a dict) capturing the internal directory structure of a tool's docker image.
ip = Input(fs.ifp) # load input.json
mf = Manifest(fs.mfp)  # load manifest.json

cb = CommandBuilder(mf, tool="biotool", filesystem=fs) # Initialize the CommandBuilder

cb.add_command(cmd="input", key="fasta").add_action(conditional_unzip_gzip)
cb.add_command(cmd="maximum_length", key="maximumLength")
cb.add_command(cmd="no-qc", key="noQC").set_kind(kind="flag")

cb.build_command(ip)
```
yields the following command:
```shell
biotool --input some_genome.fasta --maximum-length 2000 --no-qc
```
where `some_genome.fasta` exists (although the input was `some_genome.fasta.gz`!), because the action you attached to that parameter took care of that via running the function `conditional_gzip_unzip`.

## Specify constraints 

### Example: Specify constraints

To illustrate, given this `input.json`,
```json
"fasta": "some_genome.fasta",
"maximumLength": 2000,
"noQC": true
"callLargeVariants": true
```
this `run_biotool.py` implementation
```python
from batchx_dev.toolbox import FileSystem, Manifest, CommandBuilder

fs = FileSystem(tool="biotool") # data-structure (approximately a dict) capturing the internal directory structure of a tool's docker image.
ip = Input(fs.ifp) # load input.json
mf = Manifest(fs.mfp)  # load manifest.json

cb = CommandBuilder(mf, tool="biotool", filesystem=fs) # Initialize the CommandBuilder

cb.add_command(cmd="input", key="fasta")
cb.add_command(cmd="maximum_length", key="maximumLength")
cb.add_command(cmd="no-qc", key="noQC").set_kind(kind="flag")

def large_variants_constraint(input, manifest, value, k: str="maximumLength", threshold: int=200):
    """
    For constraints & actions:
        - First argument is always the Input object.
        - Second argument is always the Manifest object.
        - Third argument is always the value of the command with which the constraint is associated.
    
    Other arguments have to be keyword arguments, and can be passed whilst adding the 
    constraint to the CommandBuilder
    """
    return ip.get(k) > threshold
    
cb.add_command(cmd="large-variants", key="callLargeVariants")
    .set_kind(kind="flag")
    .add_constraint(large_variants_constraint, threshold=1000)

cb.build_command(ip)
```
yields the following command:
```shell
biotool --input some_genome.fasta --maximum-length 2000 --no-qc --large-variants
```
Whereas the same implementation, given this input,
```json
"fasta": "some_genome.fasta",
"maximumLength": 200,
"noQC": true
"callLargeVariants": true
```
would not produce any command at all and throw an error, due to the fact that `"maximumLength": 200` is incompatible with the `callLargeVariants` flag. 
Indeed, the `callLargeVariants` flag only makes sense if  `maximumLength > 1000`.

# Feature requests

Please add it to this [project board](https://github.com/orgs/batchx/projects/7).
