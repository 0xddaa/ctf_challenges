#############################################################################
# Default syslog-ng.conf file which collects all local logs into a
# single file called /var/log/messages.
#

@version: 3.8

source s_network {
	syslog(port(PORT) transport("tcp"));
};

destination d_local {
	file(
		"/dev/null"
		template("$(printf $MSG)")
	);
};

log {
	source(s_network);
	destination(d_local);
};
