========================================
BIDScoin: Coin your imaging data to BIDS
========================================

.. image:: ../bidscoin/bidscoin_logo.png
   :height: 260px
   :align: right
   :alt: Full documentation: https://bidscoin.readthedocs.io
   :target: https://bidscoin.readthedocs.io

|PyPI version| |BIDS| |PyPI - Python Version| |GPLv3| |RTD| |DOI|

BIDScoin is a user friendly `open-source <https://github.com/Donders-Institute/bidscoin>`__ Python application that converts ("coins") source-level (raw) neuroimaging data-sets to `nifti <https://nifti.nimh.nih.gov/>`__ / `json <https://www.json.org/>`__ / `tsv <https://en.wikipedia.org/wiki/Tab-separated_values>`__ data-sets that are organized according to the Brain Imaging Data Structure (`BIDS <http://bids.neuroimaging.io>`__) standard. Rather then depending on complex programmatic logic for source data-type identification, BIDScoin uses a mapping approach to discover the different source data types in your repository and convert them into BIDS data types. Different runs of source data are uniquely identified by their file system properties (e.g. file name or size) and by their attributes (e.g. ``ProtocolName`` from the DICOM header). Mapping information can be pre-specified (e.g. per site), allowing BIDScoin to make intelligent first suggestions on how to classify and convert the data. While this command-line procedure exploits all information available on disk, BIDScoin presents a `Graphical User Interface (GUI) <screenshots.html>`__ for researchers to check and edit these mappings -- bringing in the missing knowledge that often exists only in their heads.

Data conversions are performed within plugins, such as plugins that employ `dcm2niix <https://github.com/rordenlab/dcm2niix>`__, `spec2nii <https://github.com/wexeee/spec2nii>`__ or `nibabel <https://nipy.org/nibabel>`__.

BIDScoin requires no programming knowledge in order to use it, but users can use regular expression and plug-ins to further enhance BIDScoin's power and flexibilty, and deal with a wider range of source data formats.

BIDScoin is developed at the `Donders Institute <https://www.ru.nl/donders/>`__ of the `Radboud University <https://www.ru.nl/english/>`__.

BIDScoin functionality
----------------------

-  [x] DICOM source data
-  [x] PAR / REC source data (Philips)
-  [x] NIfTI source data
-  [x] Physiological logging data\*
-  [x] MR Spectroscopy data\*\*
-  [x] PET data\*
-  [x] Fieldmaps\*
-  [x] Multi-echo data\*
-  [x] Multi-coil data\*
-  [ ] Stimulus / behavioural logfiles
-  [x] Multi-echo combination
-  [x] Defacing
-  [x] Plug-ins

   ``*  = Only DICOM source data / tested for Siemens``

   ``** = Only Twix, SDAT/SPAR and P-file source data``

::

   Are you a Python programmer with an interest in BIDS who knows all about GE and / or Philips data?
   Are you experienced with parsing stimulus presentation log-files? Or do you have ideas to improve
   the this toolkit or its documentation? Have you come across bugs? Then you are highly encouraged to
   provide feedback or contribute to this project on https://github.com/Donders-Institute/bidscoin.

Note:
-----

   **The full BIDScoin documentation is hosted at** `Read the Docs <https://bidscoin.readthedocs.io>`__

   **For citation and more information, see our** `BIDScoin publication <https://www.frontiersin.org/articles/10.3389/fninf.2021.770608>`__ **in Frontiers in Neuroinformatics** (`doi: 10.3389/fninf.2021.770608 <https://doi.org/10.3389/fninf.2021.770608>`__)

   **Issues can be reported at** `Github <https://github.com/Donders-Institute/bidscoin/issues>`__

.. |PyPI version| image:: https://img.shields.io/pypi/v/bidscoin?color=success
   :target: https://pypi.org/project/bidscoin
   :alt: BIDScoin
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/bidscoin.svg
   :alt: Python 3
.. |GPLv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: GPL-v3.0 license
.. |RTD| image:: https://readthedocs.org/projects/bidscoin/badge/?version=latest
   :target: http://bidscoin.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status
.. |DOI| image:: https://img.shields.io/badge/doi-10.3389%2Ffinf.2021.770608-informational.svg
   :target: https://www.frontiersin.org/articles/10.3389/fninf.2021.770608
   :alt: DOI reference
.. |BIDS| image:: https://img.shields.io/badge/BIDS-v1.7.0-blue
   :target: https://bids-specification.readthedocs.io/en/v1.7.0/
   :alt: Brain Imaging Data Structure (BIDS)
