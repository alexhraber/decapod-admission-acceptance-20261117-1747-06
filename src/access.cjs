'use strict';
// Ownership and grants never bypass active organization membership.
exports.canRead = (actor, repository) => Boolean(
  actor && repository &&
  actor.active === true &&
  actor.organizationId === repository.organizationId &&
  (actor.id === repository.ownerId ||
    (Array.isArray(actor.repositoryIds) && actor.repositoryIds.includes(repository.id)))
);
