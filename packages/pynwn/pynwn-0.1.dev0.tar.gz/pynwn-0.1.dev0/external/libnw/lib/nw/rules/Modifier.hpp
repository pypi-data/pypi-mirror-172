#pragma once

#include "../components/ObjectBase.hpp"
#include "system.hpp"
#include "type_traits.hpp"

#include <absl/container/inlined_vector.h>

namespace nw {

enum struct ModifierType : int32_t {
    invalid = -1,
};

constexpr ModifierType make_modifier_type(int32_t id) { return static_cast<ModifierType>(id); }

template <>
struct is_rule_type_base<ModifierType> : std::true_type {
};

enum struct ModifierSource {
    unknown,
    ability,
    class_,
    environment,
    feat,
    race,
    situation,
    skill,
};

using ModifierResult = Variant<int, float>;
using ModifierFunction = std::function<ModifierResult(const ObjectBase*)>;
using ModifierSubFunction = std::function<ModifierResult(const ObjectBase*, int32_t)>;
using ModifierVsFunction = std::function<ModifierResult(const ObjectBase*, const ObjectBase*)>;
using ModifierSubVsFunction = std::function<ModifierResult(const ObjectBase*, const ObjectBase*, int32_t)>;

using ModifierVariant = Variant<
    int,
    float,
    ModifierFunction,
    ModifierSubFunction,
    ModifierVsFunction,
    ModifierSubVsFunction>;

using ModifierInputs = absl::InlinedVector<ModifierVariant, 4>;
template <typename T>
using ModifierOutputs = absl::InlinedVector<T, 4>;

struct Modifier {
    ModifierType type = ModifierType::invalid;
    ModifierInputs value;
    InternedString tagged;
    ModifierSource source = ModifierSource::unknown;
    Requirement requirement = Requirement{};
    Versus versus = {};
    int subtype = -1;
};

inline bool operator<(const Modifier& lhs, const Modifier& rhs)
{
    return std::tie(lhs.type, lhs.subtype, lhs.source) < std::tie(rhs.type, rhs.subtype, rhs.source);
}
} // namespace nw
