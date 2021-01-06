import {
  ValidationProvider as BaseValidationProvider,
  configure,
} from "vee-validate";
import { setValidationRules } from "@/validations";

const config = {
  mode: "aggressive",
};

export const ValidationProvider = (() => {
  configure(config);
  setValidationRules();
  return BaseValidationProvider;
})();
