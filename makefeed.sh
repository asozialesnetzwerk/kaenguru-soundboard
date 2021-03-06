#!/usr/bin/env bash
echo "<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Kaenguru Soundboard</title>
    <description>Ein Soundboard zu den Känguru Chroniken</description>
    <language>de-de</language>
    <link>https://asozial.org/kaenguru-soundboard</link>
    $(cat -)
    </channel>
</rss>"

