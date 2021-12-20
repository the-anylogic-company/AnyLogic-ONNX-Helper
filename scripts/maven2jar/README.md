This folder contains a dummy Maven project that is setup to allow easy downloading of Jars from one or more dependencies. There are options for downloading resources as a single jar or as a directory with all the individual jars.

For context: in the the ONNX Wrapper Library for AnyLogic, the provided runtime is for x64 architectures (i.e., 64-bit systems) and with no hardware acceleration (i.e., uses default CPU). Thus, you can use this to download alternative runtimes; see: [https://onnxruntime.ai/](https://onnxruntime.ai/).

# Usage

*Note:* Requires maven to be installed on your system.

1. Open the 'pom.xml' in any text editor

2. Under the _\<dependencies\>_ tag include any number of _\<dependency\>_ entries that you wish to download

  - You'll need to include 3 sub-tags: "groupId", "artifactId" and "version"
  
3. [OPTIONAL] If you want the output to be _either_ a single jar or a folder with individual jars, comment out one of the _\<plugin\>_ entries under the _\<build\>_ tag (see the comments in the file). 

  - You can comment one of them out (via `<!--` and `-->`).

4. Open a command prompt, navigate to the directory with the "pom.xml" file and run `mvn clean install`

Once finished, your files will be available in the "`target`" folder.
