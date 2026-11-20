from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serialize movies and reject empty required fields."""

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'release_year', 'genre']
        extra_kwargs = {
            'title': {'required': True, 'allow_blank': False},
            'director': {'required': True, 'allow_blank': False},
            'release_year': {'required': True, 'allow_null': False},
            'genre': {'required': True, 'allow_blank': False},
        }

    def validate_title(self, value):
        return self._require_non_empty(value, 'Title')

    def validate_director(self, value):
        return self._require_non_empty(value, 'Director')

    def validate_genre(self, value):
        return self._require_non_empty(value, 'Genre')

    def validate_release_year(self, value):
        if value is None:
            raise serializers.ValidationError(
                'Release year must not be empty.',
            )
        return value

    @staticmethod
    def _require_non_empty(value, field_name):
        if not value or not value.strip():
            raise serializers.ValidationError(
                f'{field_name} must not be empty.',
            )
        return value
