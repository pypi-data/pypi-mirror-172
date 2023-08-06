Example Project
===============

This library makes signal processing easy ! 
A great tool for students to easily visualise and test their sigals virtually.
know more about me : https://linktr.ee/RanitBhowmick 

Installing
============

.. code-block:: bash

    pip install wiggles

Usage
=====

.. code-block:: bash

    import wiggles.signals as sp

    x=sp.discrete([1,2,3,4,5,6,7,6,5,4,3,2,1],-2)
    x.name="x"

    x1=(2*x.TimeShift(-5))-(3*x.TimeShift(4))
    x1.name="x1"

    x2=x.operate(-1,3)+(x*x.TimeShift(-2))
    x2.name="x2"

x.compare(x1,x2)



