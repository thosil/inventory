/var/log/inventory/*.log {
	rotate 7
	daily
	missingok
	notifempty
	delaycompress
	compress
}
