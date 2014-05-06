class bdist_deb(_sdist):
	description = "make an instalable for debian/ubuntu platforms"
	user_options =  _sdist.user_options +  [
		('debian=', None, "debian dir"),
	]

	def initialize_options(self):
		_sdist.initialize_options(self)
		self.debian = None
		self.dist_dir = None
		self.keep_temp = True
		self.format = None
		self.buildcmd = None
		self.buildargs = []

	def finalize_options(self):
		_sdist.finalize_options(self)
		if self.debian == None:
			self.debian = 'debian'
		self.dist_dir = 'bdist'
		self.keep_temp = True
		self.format = 'gztar'
		self.buildcmd = 'dpkg-buildpackage'
		self.buildargs = ['-uc', '-us']

	def get_file_list(self):
		_sdist.get_file_list(self)
		for f in find_files('.', self.debian):
			self.filelist.append(f)

	def make_release_tree(self, base_dir, files):
		if os.path.isdir(base_dir):
			_remove_tree(base_dir, dry_run=self.dry_run)
		_sdist.make_release_tree(self, base_dir, files)

	def make_distribution(self):
		full_name = self.distribution.get_fullname()
		base_dir = os.path.join(self.dist_dir, full_name)
		self.make_release_tree(base_dir, self.filelist.files)
		archive_files = []
		name = self.distribution.get_name()
		version = self.distribution.get_version()
		base_name = os.path.join(self.dist_dir, name + '_' + version + '.orig')
		filename = self.make_archive(base_name, self.format, self.dist_dir, full_name)
		archive_files.append(filename)
		self.distribution.dist_files.append((self.dist_dir, '', filename))
		filename = self.make_debian(base_dir)
		self.archive_files = archive_files
		if not self.keep_temp:
			_remove_tree(base_dir, dry_run=self.dry_run)

	def make_debian(self, base_dir):
		cmd = [self.buildcmd] + self.buildargs
		try:
			os.chdir(base_dir)
			spawn(cmd, verbose=1)
		except DistutilsError as e:
			print ("Execution failed: %s" % str(e))
			return None
		name = self.distribution.get_name()
		version = self.distribution.get_version()
		return name + '_' + version + '-1_all.deb'

