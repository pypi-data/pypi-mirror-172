
DataFlow
========

|pipeline status| |coverage report| |code style| |imports| |GPLv3 license| |made-with-sphinx-doc|

DataFlow is an API to define and trigger data analysis.

Source code can be found at https://gitlab.com/alba-synchrotron/sdm/dataflow


Installation
============

Download the git repository and install from sources::

  git clone https://gitlab.com/alba-synchrotron/sdm/dataflow.git
  cd dataflow
  pip install .


Quick Start
===========

The aim of DataFlow is to chain existing operators to define a workflow and run the workflow in the user or institution infrastructure (whatever it is).

The DataFlow has been designed to make it easy and simple for the user to define a workflow and to run the job.
The definition of the operators has to handle different situations and the interaction with task environment, but DataFlow makes it also easy to do.


Hello world
-----------

Let's see how we would implement a Hello World example.


Starting from scratch, we will define a simple an operator::

  @op_decorator(BasicOP)
  def Hello(item, task):
      """
      Say Hello
      """

      if item is DONE:
          return

      person = item
      message = f"Hello {person}"
      print(message)
      return message

In this code, item will be any item arriving to the operator, and the operator has to handle it. There is a special item DONE that will be received when the user declares that no more data will be sent. In practice, the users will not work much with operators but defining workflows and operator inputs.


Once we have an operation, we can define our workflow as follows::

  @wf_decorator(wf_class=ThreadWF)
  def HelloWF(head, out):
      """
      Say hello to anyone
      """
      hello = Hello()

      head >> hello >> out

Any workflow starts with a head and ends with the out. Workflow inputs will be sent to the head by default and the result will be gathered by the out, but any intermediate item will be stored in the task environment.


Now we just need to define where will run our workflow::

  class HelloWorld(LocalJob):
      """
      Job running List workflow locally
      """
      workflow_class = HelloWF

A local job just needs to know which workflow to run. Other kinds of jobs may be more complex to configure, but this depends on the infrastructure.


Now we have all pieces in place, and our user just needs to call the job::

  people = ["Nico", "Gabriel", "Emilio", "Fernan"]

  job = job_service.create("HelloWorld")
  job.prepare()
  for p in people:
      job.submit(p)
  job.done()


.. |pipeline status| image:: https://gitlab.com/alba-synchrotron/sdm/dataflow/badges/main/pipeline.svg
   :target: https://gitlab.com/alba-synchrotron/sdm/dataflow/-/commits/main
.. |coverage report| image:: https://gitlab.com/alba-synchrotron/sdm/dataflow/badges/main/coverage.svg
   :target: https://gitlab.com/alba-synchrotron/sdm/dataflow/-/commits/main
.. |code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |imports| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://timothycrosley.github.io/isort
.. |GPLv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
.. |made-with-sphinx-doc| image:: https://img.shields.io/badge/doc-Sphinx-success.svg
   :target: http://alba-synchrotron.gitlab.io/sdm/dataflow
