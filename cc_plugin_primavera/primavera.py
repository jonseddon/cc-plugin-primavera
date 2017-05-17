#!/usr/bin/env python
"""
compliance_checker.primavera

Compliance Test Suite for the PRIMAVERA project
"""

from compliance_checker.base import BaseCheck, BaseNCCheck, Result

class PrimCheck(BaseNCCheck):
    register_checker = True
    name = 'primavera'


    @classmethod
    def make_result(cls, level, score, out_of, name, messages):
        return Result(level, (score, out_of), name, messages)

    def setup(self, ds):
        pass

    def check_global_attributes(self, ds):
        """
        Verifies the base metadata in the global attributes
        """
        attribute_fields = [
            'Conventions',
            'cake'
        ]
        level = BaseCheck.MEDIUM
        out_of = 0
        score = 0
        messages = []
        for field in attribute_fields:
            field_val = getattr(ds, field, None)
            out_of += 1
            if field_val is None:
                messages.append('%s global attribute is missing' % field)
            else:
                score += 1

            out_of += 1
            contains_string = False
            if isinstance(field_val, basestring):
                if len(field_val.strip()) > 0:
                    score += 1
                    contains_string = True
            if not contains_string:
                messages.append('%s global attribute can not be empty' % field)
        
        return self.make_result(level, score, out_of, 'Required Global Attributes', messages)


