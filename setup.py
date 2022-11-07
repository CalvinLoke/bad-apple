import os
import setuptools

# * This setup
setuptools.setup(
	name="avplib",
	version="1.0.0",
	description='AVP - ASCII Video Player. Allows you to play any video as ASCII-art.',
	keywords=['pciw', 'pciw.py'],
	packages=setuptools.find_packages(),
	author_email='semina054@gmail.com',
	url="https://github.com/romanin-rf/pciw.py",
	long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
	long_description_content_type="text/markdown",
	include_package_data=True,
	author='ProgrammerFromParlament',
	license='MIT',
	install_requires=["click", "rich", "soundfile", "opencv-python", "pillow", "pygame", "fpstimer", "ffmpeg", "moviepy", "numpy"],
    setup_requires=["click", "rich", "soundfile", "opencv-python", "pillow", "pygame", "fpstimer", "ffmpeg", "moviepy", "numpy"]
)