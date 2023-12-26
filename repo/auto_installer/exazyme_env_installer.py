from urllib.request import urlretrieve
from os.path import isfile, islink, isdir, abspath, dirname, basename
from shutil import which
from sys import argv
from os import chdir, getcwd, mkdir, remove, environ, symlink, unlink
from json import load, dump
from shlex import split as sh_split
from sys import exit, stdout
import platform
from subprocess import Popen, PIPE, TimeoutExpired


# Installer for Exazyme Virtual Environment
class Installer:
    """
    Specify the settings for your Exazyme environment here.
    THIS SECTION YOU CAN MODIFY TO YOUR LIKING
    """
    forge_version = '23.3.1-0'
    python_version = '3.11'
    project_name = 'exazyme_auto'
    working_path = 'exazyme_source'
    conda_channels = ['conda-forge']
    conda_dependencies = ['matplotlib-base']
    pip_dependencies = ['setuptools',
                        'psutil',
                        'numpy',
                        'scipy',
                        'pandas',
                        'scikit-learn',
                        'huggingface-hub']
    git_dependencies = ['https://github.com/exazyme/JaxRK.git',
                        'https://github.com/exazyme/protein_engineering_data.git',
                        'https://github.com/exazyme/enzyme_efficiency_prediction.git']
    installer = 'mamba'

    # Initialize installation
    def __init__(self):
        self.project_source = dirname(abspath(__file__))
        self.forge_source = f'{self.project_source}/forge'
        self.flags_file = f'{self.project_source}/{self.project_name}.config'

        self.flags = {'verbose': False,
                      'debug': False}
        if not isfile(self.flags_file):
            self.save_flags()
        self.load_flags()
        self.check_os()
        self.check_pre_requisites()
        self.save_flags()

    ##################################################
    #               Utility functions                #
    ##################################################

    def save_flags(self):
        """
            Store flags in the config file.
        """
        with open(self.flags_file, 'w') as handle:
            dump(self.flags, handle, indent=4)

    def load_flags(self):
        """
            Load flags from the config file.
        """
        if not isfile(self.flags_file):
            self.exit(f'Error: Configuration file not found: {self.flags_file}')
        with open(self.flags_file, "r") as handle:
            flags = load(handle)
            for flag in flags:
                self.flags[flag] = flags[flag]

    def check_flag(self, flag):
        """
        Check if a flag exists and is True
        """
        return flag in self.flags and self.flags[flag]

    # Exit installation
    @staticmethod
    def exit(message=None, args=None):
        """
            Exit with an error message
        """
        if message:
            if args:
                message = message % args
            print(message)
        exit(1)

    def check_os(self):
        """
        Check and configure operating system settings
        Returns:

        """
        if self.check_flag('os_configured'):
            print('Found OS Configuration...')
            return True

        os_check = self.execute('uname -s')
        if 'Darwin' in os_check:
            self.flags['os'] = 'MacOSX'
        elif 'Linux' in os_check:
            self.flags['os'] = "Linux"
        elif any(os in os_check for os in ['CYGWIN', 'MINGW32', 'MSYS', 'MINGW']):
            self.flags['os'] = 'Windows'
            self.exit(message='Error: Unsupported Operating System %s',
                      args='Windows')
        else:
            self.exit(message='Error: Unsupported Operating System %s',
                      args=os_check)
        self.flags['arch'] = list(platform.uname())[-2]
        self.flags['os_configured'] = True
        self.save_flags()

    # Check for pre-requisite programs
    def check_pre_requisites(self):
        if self.check_flag('prereq_configured'):
            print('Found OS Configuration...')
            return True
        if not which('bash'):
            self.exit('Error: Could not find bash')
        if not which('make'):
            self.exit('Error: Could not find make')
        if not which('gcc'):
            self.exit("Error: Could not find gcc")
        git = which('git')
        if not git:
            self.exit("Error: Could not find git")
        self.flags['git'] = git
        self.flags['prereq_configured'] = True
        self.save_flags()

    # Execute command
    def execute(self,
                command="",
                args: tuple = None,
                env: dict = None,
                realtime: bool = False,
                timeout: int = None,
                debug: bool = False,
                shell: bool = False,
                force: bool = False,
                multi: bool = False):
        """
        Execute a command.
        Args:
            command:    The command to execute
            args:       arguments to substitute into the command
                        if the command string contains %s.
            env:        Dictionary of environment variables to use.
                        If an empty dict is provided the command is
                        run with no environment variables otherwise
                        it inherits the environment variables from
                        this script.
            realtime:   Show the output of the command in real time
            timeout:    Terminate the command if it runs for more
                        than the specified number of seconds.
            debug:      Show the command input and output.
            shell:      Run the command in a separate shell.
            force:      Do not terminate even if the command is not
                        successful.
            multi:      Run multiple chained commands.
        Returns:
            output:     The output of the command.
        """
        if args:
            command = command % args
        if env != {}:
            cmd_env = environ.copy()
        else:
            cmd_env = env
        if env:
            for key in env:
                cmd_env[key] = env[key]
        if not timeout:
            timeout = 999999
        if self.flags['debug'] or debug:
            print("DEBUG INPUT: ")
            print(command)
        if not multi:
            proc = Popen(sh_split(command),
                         stderr=PIPE,
                         stdout=PIPE,
                         env=cmd_env,
                         universal_newlines=True,
                         shell=shell)
        else:
            proc = Popen(command,
                         stderr=PIPE,
                         stdout=PIPE,
                         shell=shell)
        if realtime:
            while proc.poll() is None:
                line = str(proc.stdout.readline().strip())
                print(line)
                stdout.flush()
            output = ''
        else:
            try:
                output = proc.communicate(timeout=timeout)
            except TimeoutExpired:
                if self.flags['debug'] or debug:
                    print('DEBUG: TIMEOUT')
                output = ['', '']
            if type(output[0]) is not str:
                output = [x.decode("ascii") for x in output]
            output = str(' '.join(output).strip())
        if self.flags['debug'] or debug:
            print('DEBUG OUTPUT: ')
            print(output)
        if not force and 'error' in output.lower():
            self.exit(output)
        return output

    # Clone a git repository
    def git_clone(self, git_url, env_name: str = None, pull: bool = False, install: bool = False):
        """
        Clone and potentially install a git repository from a url
        """
        if not env_name:
            env_name = self.project_name
        git_name = git_url.split('/')[-1].replace('.git', '')
        clone_output = self.execute(command='%s clone %s',
                                    args=(self.flags['git'],
                                          git_url),
                                    realtime=self.flags['verbose'],
                                    )
        if "error" in clone_output:
            raise OSError("Failed to Clone: %s" % git_url)
        if pull:
            chdir(git_name)
            self.execute(command='git pull',
                         realtime=self.flags['verbose'])

        if install:
            self.execute(command=f'{self.flags[f"{env_name}_pip"]} install -e .',
                         realtime=self.flags['verbose'])
        chdir('..')

    @staticmethod
    def conda_output_to_list(output):
        return [line.split()[0] for line in output.split("\n") if line[0] not in [" ", "#", "*", "\n"]]
    
    def link_to_bin(self, file: str = None, link_name: str = None):
        """
            Make a link to a file in the bin folder
        """
        path = f'{self.project_source}/bin'
        if not isdir(path):
            mkdir(path)
        if not link_name:
            link = f'{path}/{basename(file)}'
        else:
            link = f'{path}/{link_name}'
        if islink(link):
            unlink(link)
        symlink(src=file, dst=link)

    def check_conda_env(self, env_name: str, installer: str = None) -> list:
        """
        Check if a conda environment exists and return the
        packages installed in the environment.
        Args:
            env_name:   The name of the conda environment.
            installer:  The installer to use to check the environment.
        Returns:
            conda_pkgs: A list of the packages in the environment.
        """
        if not installer:
            installer = self.installer
        conda_out = self.execute(command=f'{self.flags[installer]} env list')
        conda_envs = self.conda_output_to_list(conda_out)
        if env_name not in conda_envs:
            self.exit(f'Could not find {env_name} virtual environment')
        conda_out = self.execute(command=f'{self.flags[installer]} list -n {env_name}')
        conda_pkgs = self.conda_output_to_list(conda_out)
        return conda_pkgs

    def check_environment_binaries(self, env_name: str = None, binaries: list = None):
        if not env_name:
            env_name = self.project_name
        if not binaries:
            binaries = []

        for binary in binaries:
            if env_name == 'base':
                path = f'{self.forge_source}/bin/{binary}'
                flag = f'{binary}'
            else:
                path = f'{self.forge_source}/envs/{env_name}/bin/{binary}'
                flag = f'{env_name}_{binary}'
            if not isfile(path):
                self.exit(f'Error: Binary {basename(binary)} not found in {env_name}')
            self.flags[flag] = path
            self.link_to_bin(path)

    ##################################################
    #        Code For Installing Environment         #
    ##################################################

    def install_forge(self):
        """
        A simple installer for MiniForge with conda and mamba
        """
        if self.check_flag('forge_installed'):
            print('Found MiniForge installation...')
            return True

        if not isdir(self.forge_source):
            mkdir(self.forge_source)
        chdir(self.forge_source)

        # Install MiniForge with mamba and conda
        print('Installing MiniForge with mamba and conda...')
        forge_base_url = f"https://github.com/conda-forge/miniforge/releases/download/{self.forge_version}/"
        download_url = f"{forge_base_url}/Mambaforge-{self.forge_version}-{self.flags['os']}-{self.flags['arch']}.sh"
        urlretrieve(download_url, filename='miniforge.sh')
        self.execute(command='bash miniforge.sh -b -u -p .',
                     realtime=self.flags['verbose'])

        self.check_environment_binaries(env_name='base',
                                        binaries=['conda', 'mamba', 'python', 'pip'])

        if self.flags['verbose']:
            print('Installed MiniForge with mamba and conda ...')
        self.flags['forge_installed'] = True
        self.save_flags()
        chdir('..')
        return True

    def install_virtual_environment(
            self,
            env_name: str,
            python: str,
            binaries: list,
            installer: str):
        """
        Install a virtual environment with a given name and python version.
        Args:
            env_name:     The name of the virtual environment
                          to install the forge folder.
            python:       The python version to install into
                          the virtual environment, e.g. 3.11.
            binaries:     A list of binary names to check for
                          and link to the bin folder.
            installer:    The installer to use for installing
                          the environment (conda or mamba).
        Returns:
            Nothing       Installs the virtual environment
                          and updates flags.
        Raises:
            TypeError:    If an unsupported installer is given.
        """
        if installer not in ['conda', 'mamba']:
            raise TypeError(f'Error: Unsupported installer: {installer}')
        self.load_flags()
        if self.check_flag(f'{env_name}_installed'):
            print('Found Virtual Environment installation...')
            return

        # Install virtual environment
        self.execute(command='%s create -n %s python=%s -y',
                     args=(self.flags[installer],
                           env_name,
                           python,
                           ),
                     realtime=self.flags['verbose'],
                     )

        self.flags[f'{env_name}_env'] = env_name
        self.check_environment_binaries(env_name=env_name,
                                        binaries=binaries)
        if self.flags['verbose']:
            print(f'Installed Virtual Environment {env_name} with python {python} and pip ...')
        self.flags[f'{env_name}_installed'] = True
        self.save_flags()
        return True

    def install_conda_dependencies(
            self,
            env_name: str,
            dependencies: list,
            channels: list,
            binaries: list,
            installer: str):
        """
        Install conda dependencies into a virtual environment
        with a given name using a given installer, channels
        and a list of dependencies to install.
        Args:
            env_name:     The name of the virtual environment
                          to install dependencies into.
            dependencies: A list of conda packages to install.
            channels:     A list of conda channels to use.
            binaries:     A list of binary names to check for
                          and link to the bin folder.
            installer:    The installer to use for installing
                          the dependencies (conda or mamba).
        Returns:
            Nothing       Installs the dependencies and updates flags.
        Raises:
            TypeError:    If an unsupported installer is given.
        """
        if installer not in ['conda', 'mamba']:
            raise TypeError(f'Error: Unsupported installer: {installer}')
        self.load_flags()
        if self.check_flag(f'{env_name}_conda_deps_installed'):
            print('Found conda dependency installation...')
            return

        conda_pkgs = self.check_conda_env(env_name=env_name,
                                          installer=installer)
        print(f'Installing conda dependencies into: {env_name}')
        conda_channels = ' '.join(['--channel ' + channel for channel in channels])

        # Install conda dependencies
        installed_dependencies = []
        for dependency in dependencies:
            if dependency not in conda_pkgs:
                print(f'Installing {dependency}...')
                installation_output = self.execute(command='%s install -n %s %s %s -y',
                                                   args=(self.flags[installer],
                                                         env_name,
                                                         conda_channels,
                                                         dependency),
                                                   env={},
                                                   realtime=self.flags['verbose'],
                                                   )
                if 'error' in installation_output.lower():
                    error = 'Error: Failed to install %s into environment: %s\n%s' % (dependency,
                                                                                      env_name,
                                                                                      installation_output,
                                                                                      )
                    self.exit(error)
                else:
                    installed_dependencies.append(dependency)

        # Check that binaries were installed and link to bin
        self.check_environment_binaries(env_name=env_name,
                                        binaries=binaries)
        self.flags[f'{env_name}_conda_deps_installed'] = True
        if self.flags['verbose']:
            print(f'Installed conda dependencies into {env_name}:')
            for dependency in installed_dependencies:
                print(dependency)
        self.save_flags()

    def install_pip_dependencies(
            self,
            env_name: str,
            dependencies: list,
            binaries: list):
        """
        Install pip dependencies into a virtual environment
        with a given name and a list of dependencies to install.
        Args:
            env_name:     The name of the virtual environment
                          to install dependencies into.
            dependencies: A list of pip packages to install.
            binaries:     A list of binary names to check for
                          and link to the bin folder.
        Returns:
            Nothing       Installs the dependencies and updates flags.
        """
        self.load_flags()
        if self.check_flag(f'{env_name}_pip_deps_installed'):
            print('Found pip dependency installation...')
            return

        # Check if virtual environment is installed
        self.check_conda_env(env_name=env_name)
        print(f'Installing pip dependencies into: {env_name}')

        # Install pip dependencies into project environment
        installed_dependencies = []
        for dependency in dependencies:
            print(f'Installing {dependency}...')
            installation_output = self.execute(command=f'{self.flags[f"{env_name}_pip"]} install {dependency}',
                                               realtime=self.flags['verbose'])
            if 'error' in installation_output.lower():
                error = 'Error: Failed to install %s into environment: %s\n%s' % (dependency,
                                                                                  env_name,
                                                                                  installation_output,
                                                                                  )
                self.exit(error)
            else:
                installed_dependencies.append(dependency)

        # Check that binaries were installed and link to bin
        self.check_environment_binaries(env_name=env_name,
                                        binaries=binaries)
        self.flags[f'{env_name}_pip_deps_installed'] = True
        if self.flags['verbose'] > 0:
            print(f'Installed pip dependencies into {env_name}:')
            for dependency in installed_dependencies:
                print(dependency)
        self.save_flags()

    def install_git_dependencies(
            self,
            env_name: str,
            dependencies: list,
            binaries: list,
            install_path: str):
        """
        Install git dependencies into a virtual environment
        with a given name and a list of dependencies to install.
        Args:
            env_name:     The name of the virtual environment
                          to install dependencies into.
            dependencies: A list of git urls to install.
            binaries:     A list of binary names to check for
                          and link to the bin folder.
            install_path: A path to clone the git repositories
                          into for future use.
        Returns:
            Nothing       Installs the dependencies and updates flags.
        """
        self.load_flags()
        if self.check_flag(f'{env_name}_git_deps_installed'):
            print('Found git dependency installation...')
            return True

        # Check if virtual environment is installed
        self.check_conda_env(env_name=env_name)
        print(f'Installing git dependencies into: {env_name}')

        if not isdir(install_path):
            mkdir(install_path)
        chdir(install_path)

        # Install pip dependencies into project environment
        installed_dependencies = []
        for dependency in dependencies:
            print(f'Installing {dependency}...')
            self.git_clone(dependency, env_name=env_name, pull=True, install=True)
            installed_dependencies.append(dependency.split('/')[-1].replace('.git', ''))

        # Check that binaries were installed and link to bin
        self.check_environment_binaries(env_name=env_name,
                                        binaries=binaries)
        self.flags[f'{env_name}_git_deps_installed'] = True
        if self.flags['verbose'] > 0:
            print(f'Installed git dependencies into {env_name}:')
            for dependency in installed_dependencies:
                print(dependency)
        self.save_flags()
        chdir('..')

        return True

    def install(self):
        """
        Specify the installation pipeline for your Exazyme environment here.
        THIS SECTION YOU CAN MODIFY TO YOUR LIKING
        """
        chdir(self.project_source)
        # Install MiniForge with mamba and conda
        self.install_forge()

        # Install base virtual environment
        self.install_virtual_environment(env_name=self.project_name,
                                         python=self.python_version,
                                         binaries=['python', 'pip'],
                                         installer='mamba')
        # Install conda dependencies
        self.install_conda_dependencies(env_name=self.project_name,
                                        dependencies=self.conda_dependencies,
                                        channels=self.conda_channels,
                                        binaries=[],
                                        installer='mamba')
        # Install pip dependencies
        self.install_pip_dependencies(env_name=self.project_name,
                                      dependencies=self.pip_dependencies,
                                      binaries=[])
        # Install git dependencies
        self.install_git_dependencies(env_name=self.project_name,
                                      dependencies=self.git_dependencies,
                                      binaries=[],
                                      install_path=self.working_path)

        # Install additional virtual environment for MMSeqs2
        self.install_virtual_environment(env_name='mmseqs',
                                         python=self.python_version,
                                         binaries=[],
                                         installer='mamba')
        # Install MMSeqs2 into its own dedicated environment
        self.install_conda_dependencies(env_name='mmseqs',
                                        dependencies=['mmseqs2'],
                                        channels=['conda-forge', 'bioconda'],
                                        binaries=['mmseqs', 'aria2c'],
                                        installer='conda')


if __name__ == "__main__":
    ex_installer = Installer()
    ex_installer.install()
