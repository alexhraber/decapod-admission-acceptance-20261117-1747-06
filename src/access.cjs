'use strict';
// Ownership and grants apply only within active organization membership.
exports.canRead = (actor, repository) => Boolean(
  actor && actor.active === true &&
  actor.organizationId === repository.organizationId &&
  (actor.id === repository.ownerId ||
    (Array.isArray(actor.repositoryIds) && actor.repositoryIds.includes(repository.id)))
);
