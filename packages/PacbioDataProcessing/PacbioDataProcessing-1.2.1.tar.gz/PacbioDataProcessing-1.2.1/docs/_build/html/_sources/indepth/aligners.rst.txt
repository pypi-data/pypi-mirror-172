.. highlight:: shell

.. _aligners:


Aligners
========

The :ref:`sm-analysis program <sm-analysis>` delegates the alignment of
BAM files to an external aligner program, which must be accessible at
runtime. The current version of |project| (v. |release|) uses the
:ref:`pbmm2` aligner by default, but :ref:`blasr` can be used as well.

The aligner program will be called on demand: if a suitable aligned
file is found, the alignment process will be skipped for that file.

By default, the aligner is searched for in the :term:`PATH`. If it is
not found in the :term:`PATH`, you will receive a common runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'pbmm2'

and the :ref:`sm-analysis program <sm-analysis>` itself will terminate.

In that case, the instructions in the following sections can help you.

.. _pbmm2:

Pbmm2
-----

The installation of the ``pbmm2`` program is described in the
`pbmm2 repository`_: ``pbmm2`` can be installed using
``conda``. Have a look at :ref:`setting_up_bioconda`, before
installing ``pbmm2``. Once ``conda`` is ready and you have an
*active* ``conda`` environment, then install ``pbmm2``:

.. code-block:: console
	    
   $ conda install pbmm2

Upon success, you will have a ``pbmm2`` executable in your conda
environment, and you will be able to pass the path to ``pbmm2``
to :ref:`sm-analysis <sm-analysis>` if needed (see
below the section on :ref:`choosing the aligner` for details).


.. _blasr:

Blasr
-----
	
.. warning::

   PacBio does not recommend to use Blasr as aligner anymore. The official
   recommendation is to use ``pbmm2``. But if, for whatever reason, you are
   interested in using Blasr to align your BAM files, keep reading. Still
   remember that since PacBio does not support Blasr, it can be a bit hard
   to get this tool in the future, and for that reason, it might happen that
   the information in this section is obsolete when you are reading it.


Probably the easiest way to install ``blasr`` is with ``conda``.
Have a look at :ref:`setting_up_bioconda`. Once those steps are followed,
and the resulting ``conda`` environment is *active*, install ``blasr``:

.. code-block:: console
	    
   $ conda install blasr

Upon success, you will be able to pass the path to the ``blasr``
executable to :ref:`sm-analysis <sm-analysis>` if needed (see below
the section on :ref:`choosing the aligner` for details).

.. warning::

   Notice that, contrary to the suggestion given in `PacBio & Bioconda`_,
   the explicit selection of the ``bioconda`` channel by means of the ``-c``
   option of ``conda install`` (e.g., ``conda install -c bioconda ...``)
   triggers a dependency error. DO NOT USE the ``-c bioconda`` option,
   just run ``conda install ...`` instead, as explained in the main text.

.. note::

   At the time of this writing, :ref:`SMRT LINK` does not contain the ``blasr``
   executable neither.


.. _choosing the aligner:
   
Telling `sm-analysis` where is the aligner
------------------------------------------

If you install |project| and try to run :ref:`sm-analysis <sm-analysis>`
but it does not find the aligner program you will, as described before,
get an error like ``No such file or directory: 'pbmm2'`` (or
``...: 'blasr'``, if you chose to use ``blasr``).

If you don't have an aligner on your target system, please read about
how to install one at :ref:`Pbmm2` or :ref:`Blasr`.

Once the aligner is installed, if it is not in the :term:`PATH`,
it is still necessary to tell :ref:`sm-analysis <sm-analysis>` where it
can be found. You need to use the command line option
:option:`sm-analysis -a`. The rest of this section explains that option
with a litle example.

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/dave/.venvs/pdp

and let us assume that ``pbmm2`` was installed in a conda environment at::

  /home/dave/miniconda3

then, after activating the |project|'s virtual environment:

.. code-block:: console

   $ source /home/dave/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``pbmm2`` by using the command
line option :option:`sm-analysis -a`, as follows:

.. code-block:: console

   $ sm-analysis -a /home/dave/miniconda3/bin/pbmm2

(the ``-a`` and ``--aligner`` options are equivalent).

On the other hand, if you want to use ``blasr``, you must explicitly tell
it to the :ref:`sm-analysis <sm-analysis>` program, using the
:option:`sm-analysis --use-blasr-aligner` option, like:

.. code-block:: console

   $ sm-analysis --use-blasr-aligner --aligner /home/dave/miniconda3/bin/blasr


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`installing conda`: https://bioconda.github.io/user/install.html#install-conda
.. _`bioconda channels`: https://bioconda.github.io/user/install.html#set-up-channels
.. _`pbmm2 repository`: https://github.com/PacificBiosciences/pbmm2
