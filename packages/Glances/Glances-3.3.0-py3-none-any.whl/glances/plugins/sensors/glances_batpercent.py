# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# SPDX-FileCopyrightText: 2022 Nicolas Hennion <nicolas@nicolargo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
#

"""Battery plugin."""

import psutil

from glances.logger import logger
from glances.plugins.glances_plugin import GlancesPlugin

# Batinfo library (optional; Linux-only)
batinfo_tag = True
try:
    import batinfo
except ImportError:
    logger.debug("batinfo library not found. Fallback to psutil.")
    batinfo_tag = False

# Availability:
# Linux, Windows, FreeBSD (psutil>=5.1.0)
# macOS (psutil>=5.4.2)
psutil_tag = True
try:
    psutil.sensors_battery()
except Exception as e:
    logger.error("Cannot grab battery status {}.".format(e))
    psutil_tag = False


class Plugin(GlancesPlugin):
    """Glances battery capacity plugin.

    stats is a list
    """

    def __init__(self, args=None, config=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args, config=config, stats_init_value=[])

        # Init the sensor class
        try:
            self.glances_grab_bat = GlancesGrabBat()
        except Exception as e:
            logger.error("Can not init battery class ({})".format(e))
            global batinfo_tag
            global psutil_tag
            batinfo_tag = False
            psutil_tag = False

        # We do not want to display the stat in a dedicated area
        # The HDD temp is displayed within the sensors plugin
        self.display_curse = False

    # @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update battery capacity stats using the input method."""
        # Init new stats
        stats = self.get_init_value()

        if self.input_method == 'local':
            # Update stats
            self.glances_grab_bat.update()
            stats = self.glances_grab_bat.get()

        elif self.input_method == 'snmp':
            # Update stats using SNMP
            # Not available
            pass

        # Update the stats
        self.stats = stats

        return self.stats


class GlancesGrabBat(object):
    """Get batteries stats using the batinfo library."""

    def __init__(self):
        """Init batteries stats."""
        self.bat_list = []

        if batinfo_tag:
            self.bat = batinfo.batteries()
        elif psutil_tag:
            self.bat = psutil
        else:
            self.bat = None

    def update(self):
        """Update the stats."""
        self.bat_list = []
        if batinfo_tag:
            # Use the batinfo lib to grab the stats
            # Compatible with multiple batteries
            self.bat.update()
            # Batinfo support multiple batteries
            # ... so take it into account (see #1920)
            # self.bat_list = [{
            #     'label': 'Battery',
            #     'value': self.battery_percent,
            #     'unit': '%'}]
            for b in self.bat.stat:
                self.bat_list.append(
                    {
                        'label': 'BAT {}'.format(b.path.split('/')[-1]),
                        'value': b.capacity,
                        'unit': '%',
                        'status': b.status,
                    }
                )
        elif psutil_tag and hasattr(self.bat.sensors_battery(), 'percent'):
            # Use psutil to grab the stats
            # Give directly the battery percent
            self.bat_list = [
                {
                    'label': 'Battery',
                    'value': int(self.bat.sensors_battery().percent),
                    'unit': '%',
                    'status': 'Charging' if self.bat.sensors_battery().power_plugged else 'Discharging',
                }
            ]

    def get(self):
        """Get the stats."""
        return self.bat_list

    @property
    def battery_percent(self):
        """Get batteries capacity percent."""
        if not batinfo_tag or not self.bat.stat:
            return []

        # Init the b_sum (sum of percent)
        # and Loop over batteries (yes a computer could have more than 1 battery)
        b_sum = 0
        for b in self.bat.stat:
            try:
                b_sum += int(b.capacity)
            except ValueError:
                return []

        # Return the global percent
        return int(b_sum / len(self.bat.stat))
