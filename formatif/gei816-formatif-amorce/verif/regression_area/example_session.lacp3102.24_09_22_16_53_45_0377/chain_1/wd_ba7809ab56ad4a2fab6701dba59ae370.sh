#!/bin/sh


/mnt/opt/cmc/tools/cadence/VMANAGER23.03.002_lnx86/tools/vmgr/jobs_manager/bin/vm_jobs_manager_watchdog -chain_dir /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_1 -launch_file /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_1/jobs_manager_launch.json -proc_dir /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/vmgr_db/proc_mgnt/projects/vmgr -chunks_dir /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/vmgr_db/chunks/projects/vmgr

exitCode=$?

if [ $exitCode -ne 0 ]; then

echo " failure job_manager_server {
description: Unable to start job manager server please look at the logs /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_1/.job_manager.out, /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_1/debug_logs.;
severity: <text>critical</text>;
failure_source_type_vmgr: pre_session;
}
" >> /tmp/vmgr-vmanager.lacp3102.uLkGXx3U1.1727038316443/job_manager_server.chunk;

/home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_1/vsof_appender.sh /tmp/vmgr-vmanager.lacp3102.uLkGXx3U1.1727038316443/job_manager_server.chunk

rm /tmp/vmgr-vmanager.lacp3102.uLkGXx3U1.1727038316443/job_manager_server.chunk;
fi

exit $exitCode;

