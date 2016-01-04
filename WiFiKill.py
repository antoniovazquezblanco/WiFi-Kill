#!/usr/bin/python2
# -*- coding: utf-8 -*-

from utils.SystemChecks import SystemChecks


if __name__ == "__main__":
	# Check if the most basic stuff in order to show a window is present...
	SystemChecks.pre_test()
	SystemChecks.post_test()

	# Now that we know that can show a window perform the rest of the checks...
	from WindowSplash import WindowSplash
	WindowSplash()

	# Ready to begin!
	from WindowMain import WindowMain
	WindowMain()
