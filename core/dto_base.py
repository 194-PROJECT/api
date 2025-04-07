from pydantic import BaseModel

class DTO(BaseModel):
    def update(self, data: dict, debug: bool = False) -> "DTO":
        update = self.model_dump()
        update.update(data)
        for k, v in self.model_validate(update).model_dump(exclude_defaults=True).items():
            if debug:
                if getattr(self, k, None) != v:
                    print(f"updating value of '{k}' from '{getattr(self, k, None)}' to '{v}'")
            setattr(self, k, v)
        return self
