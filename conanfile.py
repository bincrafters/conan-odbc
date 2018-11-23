import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class OdbcConan(ConanFile):
    name = 'odbc'
    version = '2.3.7'
    description = 'Package providing unixODBC or Microsoft ODBC'
    url = 'https://github.com/bincrafters/conan-odbc'

    license = 'LGPL/GPL'
    exports = ['LICENSE.md']

    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    _source_subfolder = 'source_subfolder'
    _install_subfolder = 'install_subfolder'

    def configure(self):
        del self.settings.compiler.libcxx  # Pure C
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        v = self.version
        source_url = 'https://iweb.dl.sourceforge.net/project/unixodbc/unixODBC/%s/unixODBC-%s.tar.gz' % (v, v)
        tools.get(source_url)
        extracted_dir = 'unixODBC-%s' % self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        if self.settings.os == 'Windows':
            return
        env_build = AutoToolsBuildEnvironment(self)
        static_flag = 'no' if self.options.shared else 'yes'
        shared_flag = 'yes' if self.options.shared else 'no'
        args = ['--enable-static=%s' % static_flag,
                '--enable-shared=%s' % shared_flag,
                '--enable-ltdl-install']

        env_build.configure(configure_dir=self._source_subfolder, args=args)
        env_build.make()
        env_build.install()

    def package(self):
        self.copy('LICENSE*', src=self._source_subfolder, dst="licenses")

    def package_id(self):
        if self.settings.os == "Windows":
            self.info.settings.arch = "ANY"
            self.info.settings.build_type = "ANY"
            self.info.settings.compiler = "ANY"
            self.info.settings.compiler.version = "ANY"
            self.info.settings.compiler.runtime = "ANY"
            self.info.settings.compiler.toolset = "ANY"

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

        if self.settings.os == 'Windows':
            self.cpp_info.libs = ['odbc32', 'odbccp32']
        else:
            self.cpp_info.libs = ['odbc', 'odbccr', 'odbcinst', 'ltdl']
            if self.settings.os == 'Linux':
                self.cpp_info.libs.append('dl')
