# Example for the Sphinx extension `tagtoctree``

The example is a Sphinx project, where the entry point is at `/example`.
In order to build the example, you should navigate to the example folder and proceed as usual to build a Sphinx project.

```bash
cd example
make html
````

You should see an output similar to this:
```bash
Running Sphinx v5.3.0
making output directory... done
WARNING: html_static_path entry '_static' does not exist
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 7 source files that are out of date
updating environment: [new config] 7 added, 0 changed, 0 removed
reading sources... [100%] subpages/page6                                                                                                                                                                                                                                                                              
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] subpages/page6                                                                                                                                                                                                                                                                               
generating indices... genindex done
writing additional pages... search done
copying static files... done
copying extra files... done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded, 1 warning.

The HTML pages are in build/html.
```