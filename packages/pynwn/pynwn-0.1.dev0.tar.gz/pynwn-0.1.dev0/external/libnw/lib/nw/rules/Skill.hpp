#pragma once

#include "../resources/Resource.hpp"
#include "Ability.hpp"
#include "system.hpp"
#include "type_traits.hpp"

#include <absl/container/flat_hash_map.h>

#include <limits>
#include <vector>

namespace nw {

struct TwoDARowView;

enum struct Skill : int32_t {
    invalid = -1,
};

constexpr Skill make_skill(int32_t id) { return static_cast<Skill>(id); }

template <>
struct is_rule_type_base<Skill> : std::true_type {
};

// Ignored 2da columns: Category, MaxCR

/// Skill definition
struct SkillInfo {
    SkillInfo() = default;
    SkillInfo(const TwoDARowView& tda);

    uint32_t name = 0xFFFFFFFF;
    uint32_t description = 0xFFFFFFFF;
    Resource icon;
    bool untrained = false;
    Ability ability = Ability::invalid;
    bool armor_check_penalty = false;
    bool all_can_use = false;
    InternedString constant;
    bool hostile = false;

    bool valid() const noexcept { return name != 0xFFFFFFFF; }
};

/// Singleton Component for Skills
struct SkillArray {
    using map_type = absl::flat_hash_map<
        InternedString,
        Skill,
        InternedStringHash,
        InternedStringEq>;

    const SkillInfo* get(Skill skill) const noexcept;
    bool is_valid(Skill skill) const noexcept;
    Skill from_constant(std::string_view constant) const;

    std::vector<SkillInfo> entries;
    map_type constant_to_index;
};

} // namespace nw
