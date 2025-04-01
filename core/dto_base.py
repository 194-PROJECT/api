from pydantic import BaseModel

class DTO(BaseModel):
    def update(self, data: dict):
        update = self.model_dump()
        update.update(data)
        for k, v in self.model_validate(update).model_dump(exclude_defaults=True).items():
            print(f"updating value of '{k}' from '{getattr(self, k, None)}' to '{v}'")
            setattr(self, k, v)
        return self
