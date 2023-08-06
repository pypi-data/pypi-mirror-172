#include "rule_helper_funcs.hpp"

#include "../constants.hpp"

#include <nw/kernel/Kernel.hpp>

namespace nwn1 {

namespace mod {

#define DEFINE_MOD(name, type)                                                     \
    nw::Modifier name(nw::ModifierVariant value, std::string_view tag,             \
        nw::ModifierSource source, nw::Requirement req, nw::Versus versus)         \
    {                                                                              \
        return nw::Modifier{                                                       \
            type,                                                                  \
            {value},                                                               \
            tag.size() ? nw::kernel::strings().intern(tag) : nw::InternedString{}, \
            source,                                                                \
            std::move(req),                                                        \
            versus,                                                                \
            -1,                                                                    \
        };                                                                         \
    }

#define DEFINE_MOD_WITH_SUBTYPE(name, subtype_type, type)                                    \
    nw::Modifier name(subtype_type subtype, nw::ModifierVariant value, std::string_view tag, \
        nw::ModifierSource source, nw::Requirement req, nw::Versus versus)                   \
    {                                                                                        \
        return nw::Modifier{                                                                 \
            type,                                                                            \
            {value},                                                                         \
            tag.size() ? nw::kernel::strings().intern(tag) : nw::InternedString{},           \
            source,                                                                          \
            std::move(req),                                                                  \
            versus,                                                                          \
            static_cast<int>(subtype),                                                       \
        };                                                                                   \
    }

DEFINE_MOD_WITH_SUBTYPE(armor_class, nw::ArmorClass, mod_type_armor_class)
DEFINE_MOD_WITH_SUBTYPE(ability, nw::Ability, mod_type_ability);
DEFINE_MOD_WITH_SUBTYPE(damage_resist, nw::Damage, mod_type_dmg_resistance);
DEFINE_MOD(hitpoints, mod_type_hitpoints)

} // namespace mod

namespace qual {

nw::Qualifier ability(nw::Ability id, int min, int max)
{
    nw::Qualifier q;
    q.selector = sel::ability(id);
    q.params.push_back(min);
    q.params.push_back(max);
    return q;
}

nw::Qualifier alignment(nw::AlignmentAxis axis, nw::AlignmentFlags flags)
{
    nw::Qualifier q;
    q.selector = sel::alignment(axis);
    q.params.push_back(static_cast<int32_t>(flags));
    return q;
}

nw::Qualifier class_level(nw::Class id, int min, int max)
{
    nw::Qualifier q;
    q.selector = sel::class_level(id);
    q.params.push_back(min);
    q.params.push_back(max);
    return q;
}

nw::Qualifier feat(nw::Feat id)
{
    nw::Qualifier q;
    q.selector = sel::feat(id);
    return q;
}

nw::Qualifier race(nw::Race id)
{
    nw::Qualifier q;
    q.selector = sel::race();
    q.params.push_back(static_cast<int32_t>(id));
    return q;
}

nw::Qualifier skill(nw::Skill id, int min, int max)
{
    nw::Qualifier q;
    q.selector = sel::skill(id);
    q.params.push_back(min);
    q.params.push_back(max);
    return q;
}

nw::Qualifier level(int min, int max)
{
    nw::Qualifier q;
    q.selector = sel::level();
    q.params.push_back(min);
    q.params.push_back(max);
    return q;
}

} // namespace qual

namespace sel {

nw::Selector ability(nw::Ability id)
{
    return {nw::SelectorType::ability, static_cast<int32_t>(id)};
}

nw::Selector alignment(nw::AlignmentAxis id)
{
    return {nw::SelectorType::alignment, static_cast<int32_t>(id)};
}

nw::Selector class_level(nw::Class id)
{
    return {nw::SelectorType::class_level, static_cast<int32_t>(id)};
}

nw::Selector feat(nw::Feat id)
{
    return {nw::SelectorType::feat, static_cast<int32_t>(id)};
}

nw::Selector level()
{
    return {nw::SelectorType::level, {}};
}

nw::Selector local_var_int(std::string_view var)
{
    return {nw::SelectorType::local_var_int, std::string(var)};
}

nw::Selector local_var_str(std::string_view var)
{
    return {nw::SelectorType::local_var_str, std::string(var)};
}

nw::Selector skill(nw::Skill id)
{
    return {nw::SelectorType::skill, static_cast<int32_t>(id)};
}

nw::Selector race()
{
    return {nw::SelectorType::race, {}};
}

} // namespace sel
} // namespace nwn1
