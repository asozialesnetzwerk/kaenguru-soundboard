#!/usr/bin/env bash
title=$1
echo "<item>
        <title>$title</title>
          <enclosure url=\"https://asozial.org/kaenguru-soundboard/files/$title\" type=\"audio/mpeg\"/>
        <guid>$title</guid>
      </item>"
