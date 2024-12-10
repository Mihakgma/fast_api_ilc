from pydantic import BaseModel, computed_field
from app.data.feed_key_words import positive_keywords, negative_keywords


class Feedback(BaseModel):
    name: str
    message: str | None = None
    pc_ip_address: str | None = None

    @computed_field
    @property
    def is_positive(self) -> bool:
        msg = self.message
        positive_words_number = sum([w in msg.lower().strip() for w in positive_keywords])
        negative_words_number = sum([w in msg.lower().strip() for w in negative_keywords])
        return positive_words_number > negative_words_number

    def __call__(self, *args, **kwargs):
        return {"name": self.name,
                "message": self.message,
                "is_positive": str(self.is_positive)}

    def __str__(self):
        output = "Name: {}\nMessage: {}\nIs Positive: {}\n".format(self.name,
                                                                   self.message,
                                                                   self.is_positive)
        return output


if __name__ == '__main__':
    feedback = Feedback(name="Dick",
                        message="Excellent course but a little shitty. Thx anyway! p.s. go to hell")
    print(feedback)
