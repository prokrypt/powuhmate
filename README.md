# powuhmate
Griffin Powermate expect script and bash example

You will need gatttool.

powermate.sh
-
it's what I started with. It's an ugly hack.

powuhmate
-
an expect script with LED control added in. It's my first time with expect scripts, so it too is an ugly hack, I guess...

There are two ways to use this. One is to have it exec your actions as desired. The second way is to remove all the exec lines from the file and pipe the output to your own script.

Features:
 - Fast and responsive
 - Minimum delay when controlling LEDs
 - Did I mention it's fast?

---

LED behavior comments taken from https://github.com/stefansundin/powermate-linux/tree/master/bluetooth
