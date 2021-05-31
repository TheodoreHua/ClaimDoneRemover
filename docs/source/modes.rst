Modes
========

Cutoff Mode
--------------
The program will delete comments older than a set amount of time (in the `config <config-options.html>`_) regardless of
whether the ToR bot responded or not. If your cutoff is too short of the bot happened to be slow, this can cause
instances where your comment gets deleted before the bot can process it, causing the post to get stuck in limbo (and
summoning angry moderators).

Bot Reply Mode
-----------------
The program will only delete comments if the ToR bot replied to it.

.. note:: Currently what the bot replied with does NOT matter (it could say that it didn't find your transcription and
          CDR would still delete that comment), if there's enough demand or need for there to be reply validation, I
          may implement it (or knowing me, whenever I get bored).

Cutoff Fallback Mode
----------------------
This is like a combination of both the :ref:`Cutoff Mode` and :ref:`Bot Reply Mode`, it'll delete when **EITHER** the
bot replies or the cutoff is reached. This carries the same risk as the :ref:`Cutoff Mode` however you can set the
cutoff to be a very long period of time (maybe a day) to avoid this issue and comments where the bot replied will still
be deleted as soon as that's detected.

My personal preference is using :ref:`Bot Reply Mode` and if I see a comment that doesn't seem to be getting deleted,
I'll scan and ignore cutoff to manually get rid of that when I deem fit. However for those who are lazy, this is the
best of both worlds (just make sure you setup the `config <config-options.html>`_ correctly)
