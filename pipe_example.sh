#!/bin/bash

echo """
[exec](pipe){echo "SUCCESS"}
[exec](menus){echo "SUCCESS"}
[submenu](really)
	[exec](a){date +[%F]}
	[exec](b){echo "success"}
[/submenu]
[exec](work!){echo "SUCCESS"}
[exec](`date`){date}

"""
