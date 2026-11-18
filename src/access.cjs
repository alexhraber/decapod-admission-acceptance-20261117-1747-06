'use strict';
// Ownership and grants are repository-scoped; neither bypasses membership.
exports.canRead = (actor, repository) => Boolean(
  actor && repository &&
  actor.active === true &&
  actor.organizationId === repository.organizationId &&
  (actor.id === repository.ownerId ||
    (Array.isArray(actor.repositoryIds) && actor.repositoryIds.includes(repository.id)))
);
