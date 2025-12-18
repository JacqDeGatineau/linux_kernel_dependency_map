## Linux Kernel Dependency Map

The current project uses Plotly and Networkx to create a network map of all of the Linux kernal modules and show their dependencies to each other.

Dependencies were loaded from  
`/lib/modules/$(uname -r)/modules.dep`

More info from [Man pages](https://www.man7.org/linux/man-pages/man5/modules.dep.5.html)

Site is live at: [https://jacqdegatineau.github.io/linux_kernel_dependency_map/](https://jacqdegatineau.github.io/linux_kernel_dependency_map/)