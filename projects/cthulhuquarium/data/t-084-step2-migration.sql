-- cthulhuquarium/t-084: drop the breeding, egg and hidden-stat schema that
-- t-082 (kind_robots #3436, 78a2b50) removed from the game on 2026-10-10.
-- Deferred until a build without any reader was live: production
-- (/api/version) runs b7a1821c, which contains 78a2b50, and no .ts/.vue/.mjs
-- file there or on main reads these columns or the egg table.
--
-- Hand-written on purpose: only the aquarium objects below. (A generated
-- `migrate dev` diff against a local database also tried to drop unrelated
-- tables that other migrations own.)

-- AquariumStock: breeding parentage and hidden individual stats.
ALTER TABLE `AquariumStock` DROP FOREIGN KEY `AquariumStock_parentAId_fkey`;
ALTER TABLE `AquariumStock` DROP FOREIGN KEY `AquariumStock_parentBId_fkey`;
DROP INDEX `AquariumStock_parentAId_idx` ON `AquariumStock`;
DROP INDEX `AquariumStock_parentBId_idx` ON `AquariumStock`;
ALTER TABLE `AquariumStock`
    DROP COLUMN `parentAId`,
    DROP COLUMN `parentBId`,
    DROP COLUMN `statCharm`,
    DROP COLUMN `statEmpathy`,
    DROP COLUMN `statGrace`,
    DROP COLUMN `statLuck`,
    DROP COLUMN `statMight`,
    DROP COLUMN `statWits`;

-- AquariumCodexEntry: the book's best-seen stats.
ALTER TABLE `AquariumCodexEntry`
    DROP COLUMN `bestStatCharm`,
    DROP COLUMN `bestStatEmpathy`,
    DROP COLUMN `bestStatGrace`,
    DROP COLUMN `bestStatLuck`,
    DROP COLUMN `bestStatMight`,
    DROP COLUMN `bestStatWits`;

-- AquariumEgg: purchased-but-unhatched eggs.
ALTER TABLE `AquariumEgg` DROP FOREIGN KEY `AquariumEgg_aquariumId_fkey`;
ALTER TABLE `AquariumEgg` DROP FOREIGN KEY `AquariumEgg_hatchedMonsterId_fkey`;
DROP TABLE `AquariumEgg`;
