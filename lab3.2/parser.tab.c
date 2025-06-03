/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 1

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 1 "parser.y"

#include <stdio.h>
#include "lexer.h"

#line 76 "parser.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "parser.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_SIZEOF = 3,                     /* SIZEOF  */
  YYSYMBOL_ENUMERATION_CONSTANT = 4,       /* ENUMERATION_CONSTANT  */
  YYSYMBOL_BOOL = 5,                       /* BOOL  */
  YYSYMBOL_CHAR = 6,                       /* CHAR  */
  YYSYMBOL_SHORT = 7,                      /* SHORT  */
  YYSYMBOL_INT = 8,                        /* INT  */
  YYSYMBOL_LONG = 9,                       /* LONG  */
  YYSYMBOL_FLOAT = 10,                     /* FLOAT  */
  YYSYMBOL_DOUBLE = 11,                    /* DOUBLE  */
  YYSYMBOL_VOID = 12,                      /* VOID  */
  YYSYMBOL_STRUCT = 13,                    /* STRUCT  */
  YYSYMBOL_UNION = 14,                     /* UNION  */
  YYSYMBOL_ENUM = 15,                      /* ENUM  */
  YYSYMBOL_IDENTIFIER = 16,                /* IDENTIFIER  */
  YYSYMBOL_STRING_LITERAL = 17,            /* STRING_LITERAL  */
  YYSYMBOL_I_CONSTANT = 18,                /* I_CONSTANT  */
  YYSYMBOL_19_ = 19,                       /* '('  */
  YYSYMBOL_20_ = 20,                       /* ')'  */
  YYSYMBOL_21_ = 21,                       /* '+'  */
  YYSYMBOL_22_ = 22,                       /* '-'  */
  YYSYMBOL_23_ = 23,                       /* '*'  */
  YYSYMBOL_24_ = 24,                       /* '/'  */
  YYSYMBOL_25_ = 25,                       /* '%'  */
  YYSYMBOL_26_ = 26,                       /* '='  */
  YYSYMBOL_27_ = 27,                       /* ','  */
  YYSYMBOL_28_ = 28,                       /* ';'  */
  YYSYMBOL_29_ = 29,                       /* '{'  */
  YYSYMBOL_30_ = 30,                       /* '}'  */
  YYSYMBOL_31_ = 31,                       /* ':'  */
  YYSYMBOL_32_ = 32,                       /* '['  */
  YYSYMBOL_33_ = 33,                       /* ']'  */
  YYSYMBOL_YYACCEPT = 34,                  /* $accept  */
  YYSYMBOL_print_l_paren = 35,             /* print_l_paren  */
  YYSYMBOL_print_r_paren = 36,             /* print_r_paren  */
  YYSYMBOL_print_l_sq_bracket = 37,        /* print_l_sq_bracket  */
  YYSYMBOL_print_r_sq_bracket = 38,        /* print_r_sq_bracket  */
  YYSYMBOL_print_l_cr_bracket = 39,        /* print_l_cr_bracket  */
  YYSYMBOL_print_r_cr_bracket = 40,        /* print_r_cr_bracket  */
  YYSYMBOL_print_tab = 41,                 /* print_tab  */
  YYSYMBOL_print_star = 42,                /* print_star  */
  YYSYMBOL_primary_expression = 43,        /* primary_expression  */
  YYSYMBOL_constant = 44,                  /* constant  */
  YYSYMBOL_enumeration_constant = 45,      /* enumeration_constant  */
  YYSYMBOL_unary_expression = 46,          /* unary_expression  */
  YYSYMBOL_47_1 = 47,                      /* $@1  */
  YYSYMBOL_unary_operator = 48,            /* unary_operator  */
  YYSYMBOL_multiplicative_expression = 49, /* multiplicative_expression  */
  YYSYMBOL_50_2 = 50,                      /* $@2  */
  YYSYMBOL_51_3 = 51,                      /* $@3  */
  YYSYMBOL_52_4 = 52,                      /* $@4  */
  YYSYMBOL_additive_expression = 53,       /* additive_expression  */
  YYSYMBOL_54_5 = 54,                      /* $@5  */
  YYSYMBOL_55_6 = 55,                      /* $@6  */
  YYSYMBOL_assignment_expression = 56,     /* assignment_expression  */
  YYSYMBOL_assignment_operator = 57,       /* assignment_operator  */
  YYSYMBOL_expression = 58,                /* expression  */
  YYSYMBOL_59_7 = 59,                      /* $@7  */
  YYSYMBOL_declaration = 60,               /* declaration  */
  YYSYMBOL_type_specifier = 61,            /* type_specifier  */
  YYSYMBOL_struct_or_union_specifier = 62, /* struct_or_union_specifier  */
  YYSYMBOL_63_8 = 63,                      /* $@8  */
  YYSYMBOL_struct_or_union = 64,           /* struct_or_union  */
  YYSYMBOL_struct_declaration_list = 65,   /* struct_declaration_list  */
  YYSYMBOL_66_9 = 66,                      /* $@9  */
  YYSYMBOL_struct_declaration = 67,        /* struct_declaration  */
  YYSYMBOL_struct_declarator_list = 68,    /* struct_declarator_list  */
  YYSYMBOL_69_10 = 69,                     /* $@10  */
  YYSYMBOL_struct_declarator = 70,         /* struct_declarator  */
  YYSYMBOL_71_11 = 71,                     /* $@11  */
  YYSYMBOL_enum_name = 72,                 /* enum_name  */
  YYSYMBOL_ident_print = 73,               /* ident_print  */
  YYSYMBOL_enum_specifier = 74,            /* enum_specifier  */
  YYSYMBOL_75_12 = 75,                     /* $@12  */
  YYSYMBOL_76_13 = 76,                     /* $@13  */
  YYSYMBOL_enumerator_list = 77,           /* enumerator_list  */
  YYSYMBOL_78_14 = 78,                     /* $@14  */
  YYSYMBOL_79_15 = 79,                     /* $@15  */
  YYSYMBOL_enumerator = 80,                /* enumerator  */
  YYSYMBOL_81_16 = 81,                     /* $@16  */
  YYSYMBOL_declarator = 82,                /* declarator  */
  YYSYMBOL_direct_declarator = 83,         /* direct_declarator  */
  YYSYMBOL_pointer = 84,                   /* pointer  */
  YYSYMBOL_translation_unit = 85           /* translation_unit  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;


/* Second part of user prologue.  */
#line 34 "parser.y"

int yylex(YYSTYPE *yylval_param, YYLTYPE *yylloc_param, yyscan_t scanner);
void yyerror(YYLTYPE *loc, yyscan_t scanner, int tab_count, const char *message);
#line 39 "parser.y"

void tabulate(int tab_count) {
    for(int i = 0; i < tab_count; i++) {
        printf("  ");
    }
}



#line 209 "parser.tab.c"


#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_uint8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL \
             && defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
  YYLTYPE yyls_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE) \
             + YYSIZEOF (YYLTYPE)) \
      + 2 * YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  30
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   112

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  34
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  52
/* YYNRULES -- Number of rules.  */
#define YYNRULES  92
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  140

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   273


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,    25,     2,     2,
      19,    20,    23,    21,    27,    22,     2,    24,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    31,    28,
       2,    26,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    32,     2,    33,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    29,     2,    30,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint8 yyrline[] =
{
       0,    52,    52,    56,    60,    64,    68,    72,    76,    80,
      84,    85,    86,    90,    94,    99,   100,   101,   101,   105,
     106,   111,   112,   112,   113,   113,   114,   114,   118,   119,
     119,   120,   120,   125,   126,   130,   134,   135,   135,   139,
     140,   145,   146,   147,   148,   149,   150,   151,   152,   153,
     154,   158,   159,   159,   160,   164,   165,   169,   170,   170,
     174,   175,   179,   180,   180,   184,   185,   185,   186,   190,
     194,   198,   199,   199,   200,   201,   201,   202,   206,   206,
     207,   207,   211,   211,   212,   217,   218,   222,   223,   227,
     228,   233,   234
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "SIZEOF",
  "ENUMERATION_CONSTANT", "BOOL", "CHAR", "SHORT", "INT", "LONG", "FLOAT",
  "DOUBLE", "VOID", "STRUCT", "UNION", "ENUM", "IDENTIFIER",
  "STRING_LITERAL", "I_CONSTANT", "'('", "')'", "'+'", "'-'", "'*'", "'/'",
  "'%'", "'='", "','", "';'", "'{'", "'}'", "':'", "'['", "']'", "$accept",
  "print_l_paren", "print_r_paren", "print_l_sq_bracket",
  "print_r_sq_bracket", "print_l_cr_bracket", "print_r_cr_bracket",
  "print_tab", "print_star", "primary_expression", "constant",
  "enumeration_constant", "unary_expression", "$@1", "unary_operator",
  "multiplicative_expression", "$@2", "$@3", "$@4", "additive_expression",
  "$@5", "$@6", "assignment_expression", "assignment_operator",
  "expression", "$@7", "declaration", "type_specifier",
  "struct_or_union_specifier", "$@8", "struct_or_union",
  "struct_declaration_list", "$@9", "struct_declaration",
  "struct_declarator_list", "$@10", "struct_declarator", "$@11",
  "enum_name", "ident_print", "enum_specifier", "$@12", "$@13",
  "enumerator_list", "$@14", "$@15", "enumerator", "$@16", "declarator",
  "direct_declarator", "pointer", "translation_unit", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-101)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-81)

#define yytable_value_is_error(Yyn) \
  0

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int8 yypact[] =
{
      71,  -101,  -101,  -101,  -101,  -101,  -101,  -101,  -101,  -101,
    -101,  -101,  -101,    37,  -101,   -10,    -1,  -101,    25,  -101,
    -101,  -101,    -2,    -3,    26,    32,  -101,  -101,  -101,    45,
    -101,  -101,    31,  -101,  -101,    -3,    61,  -101,  -101,  -101,
    -101,     2,  -101,    71,    59,   -20,    56,  -101,  -101,  -101,
    -101,  -101,  -101,  -101,  -101,  -101,    65,     2,    43,    42,
      62,  -101,    27,  -101,  -101,    71,    76,  -101,  -101,    67,
    -101,   -19,    75,     2,  -101,     2,  -101,  -101,  -101,  -101,
    -101,  -101,  -101,    66,  -101,  -101,    60,  -101,    68,  -101,
    -101,    70,    56,  -101,  -101,    76,  -101,  -101,  -101,   -11,
    -101,     2,     2,     2,     2,     2,  -101,  -101,  -101,  -101,
    -101,  -101,  -101,     2,    72,  -101,    71,  -101,  -101,  -101,
    -101,  -101,  -101,    43,    43,  -101,    28,     2,  -101,    42,
    -101,    77,  -101,     2,  -101,    42,  -101,  -101,  -101,  -101
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       0,    48,    42,    43,    44,    45,    46,    47,    41,    55,
      56,    69,    91,     0,    49,     0,     0,    50,     0,    87,
       9,    39,     0,    86,     0,    54,     6,    70,     6,    77,
       1,    92,    90,    40,     4,    85,     0,     8,    78,     6,
      89,     0,     6,     0,    58,     0,     0,    78,    17,    10,
      13,     2,    19,    20,    15,    11,    21,     0,    28,    33,
       0,     8,     0,    57,     7,     0,    72,     7,    14,    84,
      79,     0,     0,     0,    35,     0,    16,    22,    24,    26,
      29,    31,     5,    58,    60,    65,     0,    62,    68,    51,
      59,     0,     0,    71,    82,    75,     7,     2,    36,     0,
      34,     0,     0,     0,     0,     0,    88,     7,    63,    61,
      66,     7,    81,     0,     0,    74,     0,     3,    37,    23,
      25,    27,    21,    30,    32,    53,     0,     0,    73,    83,
       7,     0,    12,     0,    64,    67,    76,     3,    38,    18
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
    -101,     1,   -36,  -101,  -101,   -25,   -55,  -101,  -101,  -101,
    -101,  -101,   -56,  -101,  -101,   -35,  -101,  -101,  -101,  -100,
    -101,  -101,   -71,  -101,  -101,  -101,    85,   -43,  -101,  -101,
    -101,    44,  -101,    39,  -101,  -101,   -18,  -101,  -101,  -101,
    -101,  -101,  -101,    63,  -101,  -101,    14,  -101,    94,    87,
      80,  -101
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_uint8 yydefgoto[] =
{
       0,    73,   132,    41,   106,    37,    89,    43,    32,    54,
      55,    69,    56,    72,    57,    58,   101,   102,   103,    59,
     104,   105,    60,    75,    99,   133,    12,    13,    14,    36,
      15,    44,    65,    63,    86,   126,    87,   127,    16,    29,
      17,    91,   114,    45,    46,    92,    70,   113,    88,    23,
      24,    18
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      62,    76,    98,    38,   100,    48,    25,    66,    95,   117,
      67,    96,    93,   129,    47,    27,   118,    61,    49,    26,
      50,    51,    62,    52,    53,    30,    33,   135,    28,    34,
       1,     2,     3,     4,     5,     6,     7,     8,     9,    10,
      11,   115,    19,    19,    19,   119,   120,   121,   122,   122,
      20,    20,   125,    19,    20,    84,   128,   122,    85,    85,
      20,   -52,   138,    80,    81,    21,    77,    78,    79,   123,
     124,   122,    68,   131,    39,   136,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,   108,   109,    64,
      42,    74,   -80,    94,    97,    82,   107,   137,   116,   110,
     111,   139,   130,    31,    90,    83,   112,    22,   134,     0,
      71,    35,    40
};

static const yytype_int16 yycheck[] =
{
      43,    57,    73,    28,    75,     3,    16,    27,    27,    20,
      30,    30,    67,   113,    39,    16,    27,    42,    16,    29,
      18,    19,    65,    21,    22,     0,    28,   127,    29,    32,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    96,    16,    16,    16,   101,   102,   103,   104,   105,
      23,    23,   107,    16,    23,    28,   111,   113,    31,    31,
      23,    29,   133,    21,    22,    28,    23,    24,    25,   104,
     105,   127,    16,   116,    29,   130,     5,     6,     7,     8,
       9,    10,    11,    12,    13,    14,    15,    27,    28,    30,
      29,    26,    16,    26,    19,    33,    30,    20,    97,    31,
      30,   137,    30,    18,    65,    61,    92,    13,   126,    -1,
      47,    24,    32
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,     5,     6,     7,     8,     9,    10,    11,    12,    13,
      14,    15,    60,    61,    62,    64,    72,    74,    85,    16,
      23,    28,    82,    83,    84,    16,    29,    16,    29,    73,
       0,    60,    42,    28,    32,    83,    63,    39,    39,    29,
      84,    37,    29,    41,    65,    77,    78,    39,     3,    16,
      18,    19,    21,    22,    43,    44,    46,    48,    49,    53,
      56,    39,    61,    67,    30,    66,    27,    30,    16,    45,
      80,    77,    47,    35,    26,    57,    46,    23,    24,    25,
      21,    22,    33,    65,    28,    31,    68,    70,    82,    40,
      67,    75,    79,    40,    26,    27,    30,    19,    56,    58,
      56,    50,    51,    52,    54,    55,    38,    30,    27,    28,
      31,    30,    80,    81,    76,    40,    35,    20,    27,    46,
      46,    46,    46,    49,    49,    40,    69,    71,    40,    53,
      30,    61,    36,    59,    70,    53,    40,    20,    56,    36
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    34,    35,    36,    37,    38,    39,    40,    41,    42,
      43,    43,    43,    44,    45,    46,    46,    47,    46,    48,
      48,    49,    50,    49,    51,    49,    52,    49,    53,    54,
      53,    55,    53,    56,    56,    57,    58,    59,    58,    60,
      60,    61,    61,    61,    61,    61,    61,    61,    61,    61,
      61,    62,    63,    62,    62,    64,    64,    65,    66,    65,
      67,    67,    68,    69,    68,    70,    71,    70,    70,    72,
      73,    74,    75,    74,    74,    76,    74,    74,    78,    77,
      79,    77,    81,    80,    80,    82,    82,    83,    83,    84,
      84,    85,    85
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     0,     0,     0,     0,     0,     0,     0,     0,
       1,     1,     5,     1,     1,     1,     2,     0,     7,     1,
       1,     1,     0,     4,     0,     4,     0,     4,     1,     0,
       4,     0,     4,     1,     3,     1,     1,     0,     4,     2,
       3,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     6,     0,     8,     2,     1,     1,     2,     0,     3,
       2,     3,     1,     0,     4,     1,     0,     4,     1,     1,
       1,     6,     0,     8,     7,     0,     9,     2,     0,     2,
       0,     4,     0,     4,     1,     2,     1,     1,     6,     3,
       2,     1,     2
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (&yylloc, scanner, tab_count, YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF

/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)                                \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;        \
          (Current).first_column = YYRHSLOC (Rhs, 1).first_column;      \
          (Current).last_line    = YYRHSLOC (Rhs, N).last_line;         \
          (Current).last_column  = YYRHSLOC (Rhs, N).last_column;       \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).first_line   = (Current).last_line   =              \
            YYRHSLOC (Rhs, 0).last_line;                                \
          (Current).first_column = (Current).last_column =              \
            YYRHSLOC (Rhs, 0).last_column;                              \
        }                                                               \
    while (0)
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K])


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)


/* YYLOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

# ifndef YYLOCATION_PRINT

#  if defined YY_LOCATION_PRINT

   /* Temporary convenience wrapper in case some people defined the
      undocumented and private YY_LOCATION_PRINT macros.  */
#   define YYLOCATION_PRINT(File, Loc)  YY_LOCATION_PRINT(File, *(Loc))

#  elif defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL

/* Print *YYLOCP on YYO.  Private, do not rely on its existence. */

YY_ATTRIBUTE_UNUSED
static int
yy_location_print_ (FILE *yyo, YYLTYPE const * const yylocp)
{
  int res = 0;
  int end_col = 0 != yylocp->last_column ? yylocp->last_column - 1 : 0;
  if (0 <= yylocp->first_line)
    {
      res += YYFPRINTF (yyo, "%d", yylocp->first_line);
      if (0 <= yylocp->first_column)
        res += YYFPRINTF (yyo, ".%d", yylocp->first_column);
    }
  if (0 <= yylocp->last_line)
    {
      if (yylocp->first_line < yylocp->last_line)
        {
          res += YYFPRINTF (yyo, "-%d", yylocp->last_line);
          if (0 <= end_col)
            res += YYFPRINTF (yyo, ".%d", end_col);
        }
      else if (0 <= end_col && yylocp->first_column < end_col)
        res += YYFPRINTF (yyo, "-%d", end_col);
    }
  return res;
}

#   define YYLOCATION_PRINT  yy_location_print_

    /* Temporary convenience wrapper in case some people defined the
       undocumented and private YY_LOCATION_PRINT macros.  */
#   define YY_LOCATION_PRINT(File, Loc)  YYLOCATION_PRINT(File, &(Loc))

#  else

#   define YYLOCATION_PRINT(File, Loc) ((void) 0)
    /* Temporary convenience wrapper in case some people defined the
       undocumented and private YY_LOCATION_PRINT macros.  */
#   define YY_LOCATION_PRINT  YYLOCATION_PRINT

#  endif
# endif /* !defined YYLOCATION_PRINT */


# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value, Location, scanner, tab_count); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, yyscan_t scanner, int tab_count)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  YY_USE (yylocationp);
  YY_USE (scanner);
  YY_USE (tab_count);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep, YYLTYPE const * const yylocationp, yyscan_t scanner, int tab_count)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  YYLOCATION_PRINT (yyo, yylocationp);
  YYFPRINTF (yyo, ": ");
  yy_symbol_value_print (yyo, yykind, yyvaluep, yylocationp, scanner, tab_count);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp, YYLTYPE *yylsp,
                 int yyrule, yyscan_t scanner, int tab_count)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)],
                       &(yylsp[(yyi + 1) - (yynrhs)]), scanner, tab_count);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, yylsp, Rule, scanner, tab_count); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep, YYLTYPE *yylocationp, yyscan_t scanner, int tab_count)
{
  YY_USE (yyvaluep);
  YY_USE (yylocationp);
  YY_USE (scanner);
  YY_USE (tab_count);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}






/*----------.
| yyparse.  |
`----------*/

int
yyparse (yyscan_t scanner, int tab_count)
{
/* Lookahead token kind.  */
int yychar;


/* The semantic value of the lookahead symbol.  */
/* Default value used for initialization, for pacifying older GCCs
   or non-GCC compilers.  */
YY_INITIAL_VALUE (static YYSTYPE yyval_default;)
YYSTYPE yylval YY_INITIAL_VALUE (= yyval_default);

/* Location data for the lookahead symbol.  */
static YYLTYPE yyloc_default
# if defined YYLTYPE_IS_TRIVIAL && YYLTYPE_IS_TRIVIAL
  = { 1, 1, 1, 1 }
# endif
;
YYLTYPE yylloc = yyloc_default;

    /* Number of syntax errors so far.  */
    int yynerrs = 0;

    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

    /* The location stack: array, bottom, top.  */
    YYLTYPE yylsa[YYINITDEPTH];
    YYLTYPE *yyls = yylsa;
    YYLTYPE *yylsp = yyls;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;
  YYLTYPE yyloc;

  /* The locations where the error started and ended.  */
  YYLTYPE yyerror_range[3];



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N), yylsp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  yylsp[0] = yylloc;
  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;
        YYLTYPE *yyls1 = yyls;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yyls1, yysize * YYSIZEOF (*yylsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
        yyls = yyls1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
        YYSTACK_RELOCATE (yyls_alloc, yyls);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;
      yylsp = yyls + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex (&yylval, &yylloc, scanner);
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      yyerror_range[1] = yylloc;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END
  *++yylsp = yylloc;

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];

  /* Default location. */
  YYLLOC_DEFAULT (yyloc, (yylsp - yylen), yylen);
  yyerror_range[1] = yyloc;
  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2: /* print_l_paren: %empty  */
#line 52 "parser.y"
      { printf("("); }
#line 1394 "parser.tab.c"
    break;

  case 3: /* print_r_paren: %empty  */
#line 56 "parser.y"
      { printf(")"); }
#line 1400 "parser.tab.c"
    break;

  case 4: /* print_l_sq_bracket: %empty  */
#line 60 "parser.y"
      { printf("["); }
#line 1406 "parser.tab.c"
    break;

  case 5: /* print_r_sq_bracket: %empty  */
#line 64 "parser.y"
      { printf("]"); }
#line 1412 "parser.tab.c"
    break;

  case 6: /* print_l_cr_bracket: %empty  */
#line 68 "parser.y"
      {  printf("{\n"); tab_count +=1;}
#line 1418 "parser.tab.c"
    break;

  case 7: /* print_r_cr_bracket: %empty  */
#line 72 "parser.y"
      {printf("\n"); tab_count -=1; tabulate(tab_count); printf("}"); }
#line 1424 "parser.tab.c"
    break;

  case 8: /* print_tab: %empty  */
#line 76 "parser.y"
          {tabulate(tab_count);}
#line 1430 "parser.tab.c"
    break;

  case 9: /* print_star: %empty  */
#line 80 "parser.y"
          {printf("*");}
#line 1436 "parser.tab.c"
    break;

  case 10: /* primary_expression: IDENTIFIER  */
#line 84 "parser.y"
                     { printf("%s", (yyvsp[0].ident)); }
#line 1442 "parser.tab.c"
    break;

  case 13: /* constant: I_CONSTANT  */
#line 90 "parser.y"
                     { printf("%li", (yyvsp[0].number)); }
#line 1448 "parser.tab.c"
    break;

  case 14: /* enumeration_constant: IDENTIFIER  */
#line 94 "parser.y"
                     { printf(" %s", (yyvsp[0].ident)); }
#line 1454 "parser.tab.c"
    break;

  case 17: /* $@1: %empty  */
#line 101 "parser.y"
                 {printf("sizeof");}
#line 1460 "parser.tab.c"
    break;

  case 19: /* unary_operator: '+'  */
#line 105 "parser.y"
              {printf("+");}
#line 1466 "parser.tab.c"
    break;

  case 20: /* unary_operator: '-'  */
#line 106 "parser.y"
              {printf("-");}
#line 1472 "parser.tab.c"
    break;

  case 22: /* $@2: %empty  */
#line 112 "parser.y"
                                        {printf(" * ");}
#line 1478 "parser.tab.c"
    break;

  case 24: /* $@3: %empty  */
#line 113 "parser.y"
                                        {printf(" / ");}
#line 1484 "parser.tab.c"
    break;

  case 26: /* $@4: %empty  */
#line 114 "parser.y"
                                        {printf(" %% ");}
#line 1490 "parser.tab.c"
    break;

  case 29: /* $@5: %empty  */
#line 119 "parser.y"
                                  {printf(" + ");}
#line 1496 "parser.tab.c"
    break;

  case 31: /* $@6: %empty  */
#line 120 "parser.y"
                                  {printf(" - ");}
#line 1502 "parser.tab.c"
    break;

  case 35: /* assignment_operator: '='  */
#line 130 "parser.y"
              { printf(" = "); }
#line 1508 "parser.tab.c"
    break;

  case 37: /* $@7: %empty  */
#line 135 "parser.y"
                         { printf(", "); }
#line 1514 "parser.tab.c"
    break;

  case 39: /* declaration: type_specifier ';'  */
#line 139 "parser.y"
                             { printf(";\n\n"); }
#line 1520 "parser.tab.c"
    break;

  case 40: /* declaration: type_specifier declarator ';'  */
#line 140 "parser.y"
                                        { printf(";\n\n"); }
#line 1526 "parser.tab.c"
    break;

  case 41: /* type_specifier: VOID  */
#line 145 "parser.y"
               { printf("void "); }
#line 1532 "parser.tab.c"
    break;

  case 42: /* type_specifier: CHAR  */
#line 146 "parser.y"
               { printf("char "); }
#line 1538 "parser.tab.c"
    break;

  case 43: /* type_specifier: SHORT  */
#line 147 "parser.y"
                { printf("short "); }
#line 1544 "parser.tab.c"
    break;

  case 44: /* type_specifier: INT  */
#line 148 "parser.y"
              { printf("int "); }
#line 1550 "parser.tab.c"
    break;

  case 45: /* type_specifier: LONG  */
#line 149 "parser.y"
               { printf("long "); }
#line 1556 "parser.tab.c"
    break;

  case 46: /* type_specifier: FLOAT  */
#line 150 "parser.y"
                { printf("float "); }
#line 1562 "parser.tab.c"
    break;

  case 47: /* type_specifier: DOUBLE  */
#line 151 "parser.y"
                 { printf("double "); }
#line 1568 "parser.tab.c"
    break;

  case 48: /* type_specifier: BOOL  */
#line 152 "parser.y"
               { printf("bool "); }
#line 1574 "parser.tab.c"
    break;

  case 52: /* $@8: %empty  */
#line 159 "parser.y"
                                     { printf("%s ", (yyvsp[0].ident)); }
#line 1580 "parser.tab.c"
    break;

  case 54: /* struct_or_union_specifier: struct_or_union IDENTIFIER  */
#line 160 "parser.y"
                                     { printf("%s ", (yyvsp[0].ident)); }
#line 1586 "parser.tab.c"
    break;

  case 55: /* struct_or_union: STRUCT  */
#line 164 "parser.y"
                 {printf("struct ");}
#line 1592 "parser.tab.c"
    break;

  case 56: /* struct_or_union: UNION  */
#line 165 "parser.y"
                {printf("union ");}
#line 1598 "parser.tab.c"
    break;

  case 58: /* $@9: %empty  */
#line 170 "parser.y"
                                  {printf("\n"); tabulate(tab_count);}
#line 1604 "parser.tab.c"
    break;

  case 61: /* struct_declaration: type_specifier struct_declarator_list ';'  */
#line 175 "parser.y"
                                                { printf(";"); }
#line 1610 "parser.tab.c"
    break;

  case 63: /* $@10: %empty  */
#line 180 "parser.y"
                                     { printf(", "); }
#line 1616 "parser.tab.c"
    break;

  case 65: /* struct_declarator: ':'  */
#line 184 "parser.y"
              { printf(":"); }
#line 1622 "parser.tab.c"
    break;

  case 66: /* $@11: %empty  */
#line 185 "parser.y"
                         { printf(":"); }
#line 1628 "parser.tab.c"
    break;

  case 69: /* enum_name: ENUM  */
#line 190 "parser.y"
               {printf("enum ");}
#line 1634 "parser.tab.c"
    break;

  case 70: /* ident_print: IDENTIFIER  */
#line 194 "parser.y"
                     { printf("%s", (yyvsp[0].ident)); }
#line 1640 "parser.tab.c"
    break;

  case 72: /* $@12: %empty  */
#line 199 "parser.y"
                                                               { printf(", "); }
#line 1646 "parser.tab.c"
    break;

  case 75: /* $@13: %empty  */
#line 201 "parser.y"
                                                                           { printf(","); }
#line 1652 "parser.tab.c"
    break;

  case 78: /* $@14: %empty  */
#line 206 "parser.y"
          {tabulate(tab_count);}
#line 1658 "parser.tab.c"
    break;

  case 80: /* $@15: %empty  */
#line 207 "parser.y"
                              { printf(",\n"); tabulate(tab_count);}
#line 1664 "parser.tab.c"
    break;

  case 82: /* $@16: %empty  */
#line 211 "parser.y"
                                   { printf(" = "); }
#line 1670 "parser.tab.c"
    break;

  case 87: /* direct_declarator: IDENTIFIER  */
#line 222 "parser.y"
                     { printf(" %s", (yyvsp[0].ident)); }
#line 1676 "parser.tab.c"
    break;


#line 1680 "parser.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;
  *++yylsp = yyloc;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (&yylloc, scanner, tab_count, YY_("syntax error"));
    }

  yyerror_range[1] = yylloc;
  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval, &yylloc, scanner, tab_count);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;

      yyerror_range[1] = *yylsp;
      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp, yylsp, scanner, tab_count);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  yyerror_range[2] = yylloc;
  ++yylsp;
  YYLLOC_DEFAULT (*yylsp, yyerror_range, 2);

  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (&yylloc, scanner, tab_count, YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval, &yylloc, scanner, tab_count);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp, yylsp, scanner, tab_count);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 236 "parser.y"




int main(int argc, char *argv[]) {
    FILE *input = 0;
    int tab_count = 0;
    bool user_tab = false;
    yyscan_t scanner;
    struct Extra extra;

    if (argc > 1) {
        printf("Read file %s\n", argv[1]);
        input = fopen(argv[1], "r");
    } else {
        printf("No file in command line, use stdin\n");
        input = stdin;
    }

    init_scanner(input, &scanner, &extra);
    yyparse(scanner, tab_count);
    destroy_scanner(scanner);

    if (input != stdin) {
        fclose(input);
    }

    return 0;
}

