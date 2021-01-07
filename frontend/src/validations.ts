import { extend } from "vee-validate";
import {
  required,
  digits,
  email,
  max,
  min,
  regex,
  alpha_dash,
} from "vee-validate/dist/rules";
import {
  passwordMinLength,
  userNameMinLength,
  userNameMaxLength,
  featureTitleMinLength,
  featureTitleMaxLength,
  featureSlugMinLength,
} from "@/env";

export const setValidationRules = (): void => {
  extend("required", {
    ...required,
    message: "{_field_} can not be empty",
  });

  extend("min", {
    ...min,
    message: "{_field_} needs to be at least {length} characters. ({_value_})",
  });

  extend("max", {
    ...max,
    message: "{_field_} may not be greater than {length} characters",
  });

  extend("email", {
    ...email,
    message: "Email must be valid",
  });

  extend("regex", {
    ...regex,
    message: "{_field_} {_value_} does not match {regex}",
  });

  extend("digits", {
    ...digits,
    message: "{_field_} needs to be {length} digits",
  });

  extend("alpha_dash", {
    ...alpha_dash,
    message:
      "{_field_} may only contain alphabetic characters, numbers, dashes or underscores",
  });

  extend("passwordConfirm", {
    params: ["target"],
    validate: (value, values) => value === values["target"],
    message: "Password confirmation does not match",
  });

  extend("minPassword", {
    validate: (value) => {
      return passwordMinLength <= value.length;
    },
    message: `{_field_} needs to be at least ${passwordMinLength} characters ({_value_})`,
  });

  extend("minUserName", {
    validate: (value) => {
      return userNameMinLength <= value.length;
    },
    message: `{_field_} needs to be at least ${userNameMinLength} characters`,
  });

  extend("maxUserName", {
    validate: (value: string) => {
      return userNameMaxLength >= value.length;
    },
    message: `{_field_} may not be greater than ${userNameMaxLength} characters`,
  });

  extend("minFeatureTitle", {
    validate: (value) => {
      return featureTitleMinLength <= value.length;
    },
    message: `{_field_} needs to be at least ${userNameMinLength} characters`,
  });

  extend("maxFeatureTitle", {
    validate: (value: string) => {
      return featureTitleMaxLength >= value.length;
    },
    message: `{_field_} may not be greater than ${userNameMaxLength} characters`,
  });

  extend("minFeatureSlug", {
    validate: (value) => {
      return featureSlugMinLength <= value.length;
    },
    message: `{_field_} needs to be at least ${userNameMinLength} characters`,
  });
};
