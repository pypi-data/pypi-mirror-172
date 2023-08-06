Helps to prevent import of certain modules from certain modules.

It's useful if you have many modules in your project and want to keep them kind of
isolated.

After installing just add `import-rules` option to your `setup.cfg` file.

```
[flake8]
...
import-rules= 
	# yaml format here
	module_one:
		- allow module_two
		- deny any
	module_two:
		- deny module_one.sub.submodule
	module_two.sumbodule:
		- deny module_one
	module_three: allow any

	# this will prevent any import everywhere
	any:
		- deny any

	# default behaviour is
	any:
		- allow any

...
```

