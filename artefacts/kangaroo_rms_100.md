# KRMS1: Tracking all architectural and technical decisions
## Status
Accepted

## Context
AKangaroo is still an application yet to be tested. Hence, it makes sense to use an architecture
that can be easily managed. A Monolithic architecture with loose coupling is the architecture of choice,
as opposed to anything complex like clean architecture or microservices. As we achieve scale, we should check
the performance and change accordingly.

## Decision
We are going with a monolithic monorepo architecture to be built using React, Next, Python Flask, and SQL server runing MySQL.
We are also adopting an OOP programming paradigm to keep things relatively simple.

## Consequences
* We'll need to be careful of the quality of code being written as we expect tight coupling.

## Expectations
* 99% Availability.
* Data consistency over availability
