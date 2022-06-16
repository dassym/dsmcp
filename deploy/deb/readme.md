# Deployment
## Make archive
### File structure
[appname]_[V(major)]-[V(minor)]_[arch]  
|-DEBIAN  
|	|-control (description file)  
|	|-postinst(script file for after install)  
|-etc  
|	|-dassym  
|		|-dsmcp.ini (config file for the app)  
|-opt  
|	|-dassym  
|		|-dsmcp  
|			|-[application files]  
|-usr  
	|-bin  
	|	|-[command files]  
	|-share  
		|-applications  
		|	|-dcpbasic.desktop    
		|-icons    
			|-dassym.png    

### Description file content (DEBIAN > control)
Package: app name
Version: 0.0.0
Architecture: amd64
Maintainer: Dassym SA <dev@dassym.com>
Depends: python3 (>= 3.8.0)
Description: description

### Make the archive
```
dpkg-deb --build --root-owner-group [folder name]
```
