#!/bin/sh
unset PYTHONPATH;unset PYTHONHOME; /mnt/opt/cmc/tools/cadence/VMANAGER23.03.002_lnx86/tools/vmgr/runner/../python/bin/python /mnt/opt/cmc/tools/cadence/VMANAGER23.03.002_lnx86/tools/vmgr/runner/python/scripts/append_chunk.py -vsof /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/example_session.vsof -runs_data_dir /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/vmgr_db/chunks/projects/vmgr -session_name example_session.lacp3102.24_09_22_16_53_45_0377 -vsof_chunk $* -chain_dir /home/lacp3102/APP1/UdeS_S8_APP1/formatif/gei816-formatif-amorce/verif/regression_area/example_session.lacp3102.24_09_22_16_53_45_0377/chain_0
