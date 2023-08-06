Examples
========

Install:

.. code-block:: shell

   $ pip install super-collator


Align with relaxed spelling:

.. code-block:: python

   >>> from super_collator.strategy import CommonNgramsStrategy
   >>> from super_collator.token import SingleToken
   >>> from super_collator.super_collator import align, to_table

   >>> a = "Lorem ipsum dollar amat adipiscing elit"
   >>> b = "qui dolorem ipsum quia dolor sit amet consectetur adipisci velit"
   >>>
   >>> a = [SingleToken(s) for s in a.split()]
   >>> b = [SingleToken(s) for s in b.split()]
   >>>
   >>> c, score = align(a, b, CommonNgramsStrategy(2))
   >>> print(to_table(c))  # doctest: +NORMALIZE_WHITESPACE
   -   Lorem   ipsum -    dollar -   amat -           adipiscing elit
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit


Multiple alignment:

.. code-block:: python

   >>> from super_collator.strategy import CommonNgramsStrategy
   >>> from super_collator.token import SingleToken
   >>> from super_collator.super_collator import align, to_table

   >>> a = "qui dolorem ipsum quia dolor sit amet consectetur adipisci velit"
   >>> b = "Lorem ipsum adipiscing"
   >>> c = "Lorem dollar amat elit"
   >>>
   >>> a = [SingleToken(s) for s in a.split()]
   >>> b = [SingleToken(s) for s in b.split()]
   >>> c = [SingleToken(s) for s in c.split()]
   >>>
   >>> d, score = align(a, b, CommonNgramsStrategy(2))
   >>> e, score = align(d, c, CommonNgramsStrategy(2))
   >>> print(to_table(e))  # doctest: +NORMALIZE_WHITESPACE
   qui dolorem ipsum quia dolor  sit amet consectetur adipisci   velit
   -   Lorem   ipsum -    -      -   -    -           adipiscing -
   -   Lorem   -     -    dollar -   amat -           -          elit


Align two sentences using their part-of-speech tags only:

.. code-block:: python

   >>> from super_collator.strategy import Strategy
   >>> from super_collator.token import SingleToken
   >>> from super_collator.super_collator import align, to_table

   >>> class PosStrategy(Strategy):
   ...     def similarity(self, a, b):
   ...         return 1.0 if a.user_data == b.user_data else 0.0
   >>>
   >>> a = "it/PRP was/VBD a/DT dark/JJ and/CC stormy/JJ night/NN"
   >>> b = "it/PRP is/VBZ a/DT fine/JJ day/NN"
   >>>
   >>> a = [SingleToken(*s.split("/")) for s in a.split()]
   >>> b = [SingleToken(*s.split("/")) for s in b.split()]
   >>>
   >>> c, score = align(a, b, PosStrategy())
   >>> print(to_table(c))  # doctest: +NORMALIZE_WHITESPACE
   it was a dark and stormy night
   it is  a fine -   -      day
